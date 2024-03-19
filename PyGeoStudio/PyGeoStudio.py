# This file is part of PyGeoStudio, an interface to GeoStudio
# hydrogeotechnical software.
# Copyright (C) 2023, Moïse Rousseau
# 
# PyGeoStudio is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PyGeoStudio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import plyfile, zipfile
import os, sys
import numpy as np
import xml.etree.ElementTree as ET
import datetime
import warnings
from prettytable import PrettyTable
from bs4 import BeautifulSoup
import io

from .Analysis import Analysis
from .Geometry import Geometry
from .Context import Context
from .Material import Material
from .Reinforcement import Reinforcement
from .Mesh import Mesh
from .Results import Results
from .Function import Function
from .Dataset import Dataset, DatasetParameters

class GeoStudioFile:
  """
  Main driver of the librairy that read GeoStudio .gsz file and interface its content through Python
  
  :param geostudio_file: Path to the GeoStudio file
  :type geostudio_file: str
  """
  def __init__(self, geostudio_file):
    self.f_src = geostudio_file
    self.geometries = []
    self.meshes = []
    self.analyses = []
    self.contexts = []
    self.datasets = []
    self.materials = []
    self.reinforcements = []
    self.xml_items = []
    self.functions = {
      "Material" : {
        "Hydraulic" : {
          "KFns" : [],
          "VolWCFns" : [],
        },
      },
      "Boundary" : {
        "Hydraulic" : {
          "BoundFns" : [],
        },
      },
    }
    self.initialize()
    return

  def __getitem__(self, item):
    if item == "Analyses": return self.analyses
    elif item == "Materials": return self.materials
    elif item == "Reinforcements": return self.reinforcements
    elif item == "Functions": return self.__functionToList__(self.functions)
    else:
      raise KeyError(f"There is no item \"{item}\" accessible through PyGeoStudio class")

  def initialize(self):
    """
    :meta private:
    """
    #open file
    if os.path.isfile(self.f_src):
      src = zipfile.ZipFile(self.f_src, 'r')
    else:
      raise IOError(f"File {self.f_src} doesn't exist in the current directory")
    #parse geoslope input
    self.prefix = self.f_src.split('/')[-1][:-4]
    try:
      self.main_xml = ET.parse(src.open(prefix+'.xml'))
    except:
      #search for an xml file
      file_list = src.infolist()
      found = False
      for f in file_list:
        f = f.filename
        if f.split('.')[-1] == "xml":
          found = True
          break
      if not found:
        raise IOError(f"There is no xml configuration file in archive {self.f_src}. Is this a GeoStudio study ?")
      warnings.warn(f"Unable to find GeoStudio configuration file \"{self.prefix}.xml\", but a configuration file named {f} was found. We will continue with this file. We recommand not renaming GeoStudio study.")
      self.main_xml = ET.parse(src.open(f))
      self.prefix = '.'.join(f.split('/')[-1].split('.')[:-1])
    root = self.main_xml.getroot()
    for element in root:
      if element.tag == "FileInfo":
        self.f_src_info = element.attrib
        self.xml_items.append("FileInfo")
      elif element.tag == "Geometries":
        self.__readGeometry__(element)
        self.xml_items.append("Geometries")
      elif element.tag == "Analyses":
        self.__readAnalysis__(element)
        self.xml_items.append("Analyses")
      elif element.tag == "Contexts":
        #context define the material properties associated with the analysis and BC
        self.__readContexts__(element)
        self.xml_items.append("Contexts")
      elif element.tag == "Materials":
        self.__readMaterials__(element)
        self.xml_items.append("Materials")
      elif element.tag == "Reinforcements":
        self.__readReinforcements__(element)
        self.xml_items.append("Reinforcements")
      elif element.tag == "Functions":
        self.__readFunctions__(element)
        self.xml_items.append("Functions")
      elif element.tag == "DataSets":
        self.__readDataSets__(element)
        self.xml_items.append("DataSets")
      else:
        #store the item for the write method
        self.xml_items.append(element)

    # Parse meshes used in the study
    for geom in self.geometries:
      meshid_geom = geom["MeshId"]
      if meshid_geom is None: continue
      f_mesh = f"mesh_{meshid_geom}.ply"
      try:
        mesh_obj = Mesh(meshid_geom, src.open(f_mesh))
      except:
        warnings.warn(f"Unable to find mesh defined for Geometry Name \"{geom['Name']}\" under {f_mesh}")
      self.meshes.append(mesh_obj)
      geom.mesh = mesh_obj

    #make function accessible from object
    for mat in self.materials:
      if mat["SeepModel"] == "SatUnsat":
        index = mat["Hydraulic"]["KFnNum"]
        for fun in self.functions["Material"]["Hydraulic"]["KFns"]:
          if fun["ID"] == index:
            mat["Hydraulic"]["KFn"] = fun
            break
        index = mat["Hydraulic"]["VolWCFnNum"]
        for fun in self.functions["Material"]["Hydraulic"]["VolWCFns"]:
          if fun["ID"] == index:
            mat["Hydraulic"]["VolWCFn"] = fun
            break

    # Create analysis structure, i.e. define Geometry, Mesh, Context and Results
    for analysis in self.analyses:
      geom = self.getGeometryByID(analysis["GeometryId"])
      analysis["Geometry"] = geom
      analysis["Results"] = Results(
        self.f_src,
        analysis,
        mesh=geom.mesh,
      )
    for context in self.contexts:
      analysis = self.getAnalysisByID(context["AnalysisID"])
      analysis["Context"] = context

    src.close()

    return

  def __readGeometry__(self,element):
    self.n_geometry = int(element.attrib["Len"])
    for i in range(self.n_geometry):
      new_geom = Geometry()
      new_geom.read(element[i])
      self.geometries.append(new_geom)
    return

  def __readAnalysis__(self,element):
    self.n_analysis = int(element.attrib["Len"])
    for i in range(self.n_analysis):
      new_analysis = Analysis(element[i])
      self.analyses.append(new_analysis)
    return

  def __readContexts__(self, element):
    n_contexts = int(element.attrib["Len"])
    for i in range(n_contexts):
      new_context = Context(element[i])
      self.contexts.append(new_context)
    return

  def __readMaterials__(self, element):
    self.n_materials = int(element.attrib["Len"])
    for i in range(self.n_materials):
      new_mat = Material(element[i])
      self.materials.append(new_mat)
    return

  def __readReinforcements__(self, element):
    self.n_reinforcements = int(element.attrib["Len"])
    for i in range(self.n_reinforcements):
      reinf_ = element[i]
      new_reinf = Reinforcement(reinf_)
      self.reinforcements.append(new_reinf)
    return

  def __readFunctions__(self, et, current=[]):
    s = self.functions
    for x in current: s = s[x]
    for d in et:
      if d.tag not in s:
        s[d.tag] = d
      elif isinstance(s[d.tag], dict):
        current.append(d.tag)
        self.__readFunctions__(d, current)
      elif isinstance(s[d.tag], list):
        current.append(d.tag)
        for infun in d:
          fun = Function(infun)
          fun.data["Types"] = [x for x in current]
          s[d.tag].append(fun)
        current.pop()
    if current: current.pop()
    return

  def __readDataSets__(self, element):
    self.n_datasets = int(element.attrib["Len"])
    for i in range(self.n_datasets):
      dataset_ = element[i]
      new_dataset = Dataset(dataset_, self.f_src)
      self.datasets.append(new_dataset)
    return

  def __getXByName_internal__(self, data, data_name, name):
    for x in data:
      if x["Name"] == name:
        return x
    raise ValueError(f"{data_name} {name} not found in file.")

  def showAnalysisTree(self):
    """
    Print the analysis tree in the GeoStudio file with analysis ID, name and parent ID if defined.
    """
    print(f"GeoStudio file: {self.f_src}")
    res = PrettyTable()
    res.field_names = ["ID","Name","ParentID"]
    for analysis in self.analyses:
      res.add_row([analysis['ID'],analysis['Name'],analysis['ParentID']])
    print(res)
    return

  def getAnalysisByName(self, name):
    """
    Return the analysis in the analysis tree corresponding to the name given.
    
    :param name: Name of the analysis (must match the name in the analysis tree)
    :type name: str
    :raise ValueError: No analysis found with the given name.
    :return: The analysis with the given name.
    :rtype: Analysis object
    """
    return self.__getXByName_internal__(self.analyses, "Analysis", name)

  def getAnalysisByID(self, ID):
    """
    Return the analysis in the analysis tree corresponding to the ID given.
    
    :param ID: ID of the analysis
    :type ID: int
    """
    for analysis in self.analyses:
      if analysis["ID"] == ID:
        return analysis
    raise ValueError(f"Analysis ID {ID} not found in file.")

  def showGeometries(self):
    """
    Print the geometries definied within the GeoStudio file
    """
    res = PrettyTable()
    res.field_names = ["Name", "Analysis ID defined"]
    for geom_id,geom in enumerate(self.geometries):
      analysis_defined = []
      for analysis in self.analyses:
        if analysis["GeometryId"] == geom_id+1:
          analysis_defined.append(str(analysis["ID"]))
      res.add_row([geom['Name'],",".join(analysis_defined)])
    print(res)
    return

  def getGeometryByID(self, ID):
    """
    Return the geometry corresponding to the ID given.
    
    :param ID: ID of the geometry
    :type ID: int
    :meta private:
    """
    if ID > len(self.geometries): raise ValueError(f"No such geometry with ID {ID}")
    return self.geometries[ID-1]

  def showMaterials(self, detail=0):
    """
    Print the material defined within the GeoStudio file.
    
    :param detail: Show a table listing minimal properties of the materials (0) or print exhaustive information (1)
    :type detail: int (0 or 1)
    """
    if detail != 0:
      for mat in self.materials: #print the material name properties
        print(mat)
        print("----------------------")
    else:
      res = PrettyTable()
      res.field_names = ["ID","Name","Seep Model","Slope Model"]
      for mat in self.materials:
        res.add_row([mat['ID'],mat['Name'],mat['SeepModel'],mat['SlopeModel']])
      print(res)
    return

  def getMaterialByName(self, name):
    """
    Return the material corresponding to the name given.
    
    :param name: Name of the material
    :type name: str
    """
    for mat in self.materials:
      if mat["Name"] == name:
        return mat
    raise ValueError(f"Material {name} not found in file.")

  def getMaterialByID(self, ID):
    """
    Return the material corresponding to the ID given.
    
    :param ID: ID of the material
    :type ID: int
    """
    for mat in self.materials:
      if mat["ID"] == ID:
        return mat
    raise ValueError(f"Material ID {ID} not found in file.")

  def showReinforcements(self, detail=0):
    """
    Print the reinforcements defined within the GeoStudio file.
    
    :param detail: Show a table listing minimal properties of the reinforcements (0) or print exhaustive information (1)
    :type detail: int (0 or 1)
    """
    if detail != 0:
      for reinf in self.reinforcements: #print the material name properties
        print(reinf)
        print("----------------------")
    else:
      res = PrettyTable()
      res.field_names = ["ID","Name", "Type"]
      for reinf in self.reinforcements:
        res.add_row([reinf['ID'],reinf['Name'],reinf['Type']])
      print(res)
    return

  def getReinforcementByName(self, name):
    """
    Return the reinforcement corresponding to the name given.
    
    :param name: Name of the reinforcement
    :type name: str
    """
    for x in self.reinforcements:
      if x["Name"] == name:
        return x
    raise ValueError(f"Reinforcement {name} not found in file.")

  def getReinforcementByID(self, ID):
    """
    Return the reinforcement corresponding to the ID given.
    
    :param ID: ID of the material
    :type ID: int
    """
    for x in self.reinforcements:
      if x["ID"] == ID:
        return x
    raise ValueError(f"Reinforcements ID {ID} not found in file.")

  def showFunctions(self):
    """
    Print a table showing the functions defined within the GeoStudio file.
    """
    res = PrettyTable()
    res.field_names = ["Function Name","Types"]
    l = self.__functionToList__(self.functions)
    for function in l:
      res.add_row([function['Name'],",".join(function['Types'])])
    print(res)
    return

  def getFunctionByName(self, name, type_filter=None):
    """
    Return the Function corresponding to the name given. Can return the Function only if it is a given type.
    
    :param name: The name of the function in GeoStudio study
    :type name: str
    :param type_filter: Select Function belonging to the type given. Example ``["Material", "VolWCFn"]`` for searching only through functions applying to Material and of type Volumic Water Content.
    :type type_filter: list of str
    :meta private:
    """
    l = self.__functionToList__(self.functions)
    for func in l:
      if func["Name"] == name:
        return func
    raise ValueError(f"No function nammed {name} in file.")
    return

  def showDatasets(self):
    """
    Print a table showing the dataset defined within the GeoStudio file.
    """
    res = PrettyTable()
    res.field_names = ["ID","Dataset","Parameters"]
    l = self.datasets
    for dataset in self.datasets:
      res.add_row([dataset['ID'], dataset['Name'],dataset['Parameters']])
    print(res)
    return

  def getDatasetByName(self, name):
    """
    Return the dataset corresponding to the name given.
    
    :param name: Name of the dataset
    :type name: str
    """
    return self.__getXByName_internal__(self.datasets, "Dataset", name)

  def createNewDataset(self, name, parameters):
    """
    Create a new dataset
    
    :param name: Name of the new dataset
    :type name: str
    :param params: List of the parameter name. Must match the available dataset parameter in GeoStudio: {self.dataset_parameters.keys()}
    :type params: list
    """
    dataset = Dataset()
    dataset["Name"] = name
    dataset["ID"] = max([x["ID"] for x in self.datasets])+1
    dataset["CsvID"] = max([x["CsvID"] for x in self.datasets])+1
    dataset.setDataParameters(parameters)
    self.datasets.append(dataset)
    return dataset

  def genConfigurationFile(self):
    """
    Generate the main xml file and return it as a string
    
    :meta private:
    """
    #build new ET
    src_root = self.main_xml.getroot()
    out_root = ET.Element(src_root.tag)
    out_root.attrib = src_root.attrib
    for element in self.xml_items:
      if element == "FileInfo":
        sub = ET.SubElement(out_root, "FileInfo")
        sub.attrib = self.f_src_info.copy()
        sub.attrib["LastAuthor"] = "Modified by PyGeoStudio"
        sub.attrib["RevNumber"] = str(int(sub.attrib["RevNumber"])+1)
        x = datetime.datetime.now()
        sub.attrib["Date"] = x.strftime('%m') + '-' + x.strftime('%d') + '-' + x.strftime('%G')
        sub.attrib["Time"] = x.strftime("%X")
      elif element == "Geometries":
        sub = ET.SubElement(out_root, "Geometries")
        sub.attrib = {"Len":str(len(self.geometries))}
        for geom in self.geometries:
          sub_geom = ET.SubElement(sub, "Geometry")
          geom.__write__(sub_geom)
      elif element == "Analyses":
        sub = ET.SubElement(out_root, "Analyses")
        sub.attrib = {"Len":str(len(self.analyses))}
        for analysis in self.analyses:
          sub_analysis = ET.SubElement(sub, "Analysis")
          analysis.__write__(sub_analysis)
      elif element == "Contexts":
        sub = ET.SubElement(out_root, "Contexts")
        sub.attrib = {"Len":str(len(self.contexts))}
        for context in self.contexts:
          sub_context = ET.SubElement(sub, "Context")
          context.__write__(sub_context)
      elif element == "Materials":
        sub = ET.SubElement(out_root, "Materials")
        sub.attrib = {"Len":str(len(self.materials))}
        for mat in self.materials:
          sub_mat = ET.SubElement(sub, "Material")
          mat.__write__(sub_mat)
      elif element == "Reinforcements":
        sub = ET.SubElement(out_root, "Reinforcements")
        sub.attrib = {"Len":str(len(self.reinforcements))}
        for reinf in self.reinforcements:
          sub_reinf = ET.SubElement(sub, "Reinforcement")
          reinf.__write__(sub_reinf)
      elif element == "Functions":
        sub = ET.SubElement(out_root, "Functions")
        self.__writeFunctions__(self.functions, sub)
      elif element == "DataSets":
        sub = ET.SubElement(out_root, "DataSets")
        sub.attrib = {"Len":str(len(self.datasets))}
        for dataset in self.datasets:
          sub_data = ET.SubElement(sub, "DataSet")
          dataset.__write__(sub_data)
      else:
        #store the item for the write method
        out_root.append(element)
    tree_string = ET.tostring(out_root, encoding="UTF-8", xml_declaration=True, method="xml")
    return tree_string

  def __writeFunctions__(self, d, et):
    for k,v in d.items():
      if isinstance(v, dict):
        sub = ET.SubElement(et, k)
        self.__writeFunctions__(v, sub)
      elif isinstance(v, list): #write functions
        sub = ET.SubElement(et, k)
        sub.attrib = {"Len":str(len(v))}
        for fun in v:
          sub_fun = ET.SubElement(sub, k[:-1])
          fun.__write__(sub_fun)
      elif isinstance(v, ET.Element):
          et.append(v)
      else:
        raise RuntimeError("Error writing Functions... Did you modify the Function attribute yourself ? If no, this is an please contact for assistance")
    return

  def __functionToList__(self, d, l=[]):
    for k,v in d.items():
      if isinstance(v, dict):
        self.__functionToList__(v, l)
      elif isinstance(v, list):
        for fun in v:
          l.append(fun)
    return l

  def save(self):
    """
    Save the modification made by PyGeoStudio to the current GeoStudio file.
    """
    # zipfile can't overwrite file.
    # So we must write the modified study in a BytesIO then overwrite the results
    temp_space = io.BytesIO()
    self.saveAs(temp_space)
    # overwrite current study
    zip_mem = zipfile.ZipFile(temp_space, 'r') #temp zip in memory
    zip_out = zipfile.ZipFile(
      self.f_src, 'w',
      compression=zipfile.ZIP_DEFLATED,
      compresslevel=5,
    )
    for f in zip_mem.namelist():
      zip_out.writestr(f, data=zip_mem.read(f))
    zip_mem.close()
    zip_out.close()
    return

  def saveAs(self, f_out, compresslevel=5):
    """
    Write the (modified) study under a new file. Note the results are not copied to the new study.
    
    :param f_out: Name of the new file (must be different than the input)
    :type f_out: str
    :param compresslevel: Level of compression of the output file from 0 (uncompressed) to 9 (fully compressed) (optional, default=1)
    :type compresslevel: int
    """
    if isinstance(f_out, io.BytesIO):
      # if BytesIO, this mean save() method
      zip_out = zipfile.ZipFile(f_out, 'a')
      prefix = self.f_src.split('/')[-1][:-4]
    else:
      # create output
      if f_out == self.f_src:
        raise ValueError("The new file has the same name than the input file. Please write within another file or use the save() method")
      ext = f_out.split('.')[-1]
      if ext != "gsz":
        f_out += ".gsz"
      prefix = f_out.split('/')[-1][:-4]
      zip_out = zipfile.ZipFile(
        f_out, mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=compresslevel
      )
    # Write
    zip_src = zipfile.ZipFile(self.f_src, 'r') #source geostudio zip
    for dataset in self.datasets:
      dataset_out = zip_out.open(f"dataset_{dataset['CsvID']}.csv", 'w')
      arr = dataset.getData()
      np.savetxt(
        dataset_out,
        np.append(
          np.arange(1,arr.shape[0]+1)[:,None],
          arr,
          axis=1,
        ),
        delimiter=',',
        header = "Undefined," + ','.join(dataset["Parameters"]),
        fmt = ["%i"] + ["%.6e" for x in dataset["Parameters"]],
        comments = "",
      )
      dataset_out.close()
    for f in zip_src.namelist():
      if f.split('.')[-1] == "xml": #main xml file
        main_xml_str = self.genConfigurationFile()
        zip_out.writestr(f.replace(self.prefix,prefix), data=main_xml_str)
      elif ".csv" in f and "dataset" in f:
        continue
      #TODO: meshes
      else:
        zip_out.writestr(f, data=zip_src.read(f))
    zip_src.close()
    zip_out.close()
    # Write meshes
#    for mesh in self.meshes:
#      byte_str = io.BytesIO()
#      mesh.write(byte_str)
#      mesh_name = "mesh_" + str(mesh.mesh_id) + ".ply"
#      zip_out.writestr(mesh_name, data=byte_str.getvalue())
    if not isinstance(f_out, io.BytesIO):
      print(f"GeoStudio study successfully written in {f_out}")
    return

