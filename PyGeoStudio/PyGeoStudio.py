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
    self.materials = []
    self.reinforcements = []
    self.xml_items = []
    self.initialize()
    return

  def __getitem__(self, item):
    match item:
      case "Analyses": return self.analyses
      case "Materials": return self.materials
      case "Reinforcements": return self.reinforcements
      case "Functions": return self.mesh_id
      case _:
        raise ValueError(f"No accessible item of name {item} through PyGeoStudio interface")

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
    prefix = self.f_src.split('/')[-1][:-4]
    self.main_xml = ET.parse(src.open(prefix+'.xml'))
    root = self.main_xml.getroot()
    for element in root:
      #print(element.tag)
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
      else:
        #store the item for the write method
        self.xml_items.append(element)

    # Parse meshes used in the study
    for geom in self.geometries:
      meshid_geom = geom["MeshId"]
      f_mesh = f"mesh_{meshid_geom}.ply"
      try:
        mesh_obj = Mesh(meshid_geom, src.open(f_mesh))
      except:
        warnings.warn(f"Unable to find mesh defined for Geometry Name \"{geom['Name']}\" under {f_mesh}")
      self.meshes.append(mesh_obj)
      geom.mesh = mesh_obj

    # Create analysis structure, i.e. define Geometry, Mesh, Context and Results
    for analysis in self.analyses:
      geom = self.getGeometryByID(analysis["GeometryId"])
      analysis["Geometry"] = geom
      analysis["Results"] = Results(
        self.f_src,
        analysis["Name"],
        time=tuple(float(x["ElapsedTime"]) for x in analysis["TimeIncrements"]["TimeSteps"]) if analysis["Method"] == "Transient" else [-1],
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
      new_reinf = Reinforcement({x.tag:x.text for x in reinf_})
      self.reinforcements.append(new_reinf)
    return


  def showAnalysisTree(self):
    """
    Print the analysis tree in the GeoStudio file with analysis ID, name and parent ID if defined.
    """
    print(f"GeoStudio file: {self.f_src}")
    #first pass, those with no parentID
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
    for analysis in self.analyses:
      if analysis["Name"] == name:
        return analysis
    raise ValueError(f"Analysis {name} not found in file.")

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
      else:
        #store the item for the write method
        out_root.append(element)
    tree_string = ET.tostring(out_root, encoding="UTF-8", xml_declaration=True, method="xml")
    #tree_string = BeautifulSoup(tree_string, 'xml').prettify()
    return tree_string

  def save(self):
    """
    Save the modification made by PyGeoStudio to the current GeoStudio file.
    """
    prefix = self.f_src.split('/')[-1][:-4]
    # Write main conf file
    zip_out = zipfile.ZipFile(self.f_src, 'a')
    main_xml_str = self.genConfigurationFile()
    zip_out.writestr(prefix + ".xml", data=main_xml_str)
    # TODO: write meshes when we can modify it!
    return

  def saveAs(self, f_out=None, compresslevel=3):
    """
    Write the (modified) study under a new file. Note the results are not copied to the new study.
    
    :param f_out: Name of the new file (must be different than the input)
    :type f_out: str
    :param compresslevel: Level of compression of the output file from 0 (uncompressed) to 9 (fully compressed) (optional, default=1)
    :type compresslevel: int
    """
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
    # Write main conf file
    main_xml_str = self.genConfigurationFile()
    zip_out.writestr(prefix + ".xml", data=main_xml_str)
    # Write meshes
    for mesh in self.meshes:
      byte_str = io.BytesIO()
      mesh.write(byte_str)
      mesh_name = "mesh_" + str(mesh.mesh_id) + ".ply"
      zip_out.writestr(mesh_name, data=byte_str.getvalue())
    zip_out.close()
    print(f"GeoStudio study successfully written in {f_out}")
    return
  
