import plyfile, zipfile
import os, sys
import numpy as np
import xml.etree.ElementTree as ET
import datetime
from prettytable import PrettyTable

from .Analysis import Analysis 
from .Geometry import Geometry 
from .Context import Context
from .Material import Material
from .Reinforcement import Reinforcement
from .Mesh import Mesh
from .Results import Results

class GeoStudioFile:
  def __init__(self, geostudio_file, mode='r'):
    self.f_src = geostudio_file
    self.src = None
    self.open_mode = mode
    
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
  
  def showAnalysisTree(self, detail_level=0):
    print(f"GeoStudio file: {self.f_src}")
    #first pass, those with no parentID
    res = PrettyTable()
    res.field_names = ["ID","Name","ParentID"]
    for analysis in self.analyses:
      res.add_row([analysis['ID'],analysis['Name'],analysis['ParentID']])
    print(res)
    return
  
  def initialize(self):
    #open file
    if os.path.isfile(self.f_src):
      self.src = zipfile.ZipFile(self.f_src, self.open_mode)
    else:
      print(f"File {self.f_src} doesn't exist in the current directory")
      raise ValueError
    #parse geoslope input
    prefix = self.f_src.split('/')[-1][:-4]
    self.main_xml = ET.parse(self.src.open(prefix+'.xml'))
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
    
    #Create analysis structure, i.e. define Geometry, Mesh, Context and Results
    for analysis in self.analyses:
      geom = self.getGeometryByID(analysis["GeometryId"])
      f_mesh = analysis["Name"].replace('/','&3')+"/Mesh.ply"
      geom.mesh = Mesh(self.src.open(f_mesh))
      analysis["Geometry"] = geom
      analysis["Results"] = Results(
        self.src,
        analysis["Name"],
        time=tuple(float(x["ElapsedTime"]) for x in analysis["TimeIncrements"]["TimeSteps"]) if analysis["Method"] == "Transient" else [-1],
        mesh=geom.mesh,
      )
    for context in self.contexts:
      analysis = self.getAnalysisByID(context["AnalysisID"])
      analysis["Context"] = context
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
      new_analysis = Analysis({})#{x.tag:x.text for x in element[i]})
      new_analysis.read(element[i])
      self.analyses.append(new_analysis)
    return
  
  def __readContexts__(self, element):
    n_contexts = int(element.attrib["Len"])
    for i in range(n_contexts):
      new_context = Context({})
      new_context.read(element[i])
      self.contexts.append(new_context)
    return
  
  def __readMaterials__(self, element):
    self.n_materials = int(element.attrib["Len"])
    for i in range(self.n_materials):
      mat_ = element[i]
      new_mat = Material()
      new_mat.read(mat_)
      self.materials.append(new_mat)
    return
      
  def __readReinforcements__(self, element):
    self.n_reinforcements = int(element.attrib["Len"])
    for i in range(self.n_reinforcements):
      reinf_ = element[i]
      new_reinf = Reinforcement({x.tag:x.text for x in reinf_})
      self.reinforcements.append(new_reinf)
    return
  
  def printGeometries(self):
    print(self.geometries)
    return
  
  def getGeometryByID(self, id_):
    """
    Return the geometry corresponding to the ID given
    """
    if id_ > len(self.geometries): raise ValueError(f"No such geometry with ID {id_}")
    return self.geometries[id_-1]
  
  def getAnalysisByID(self, id_):
    """
    Return the analysis in the analysis tree corresponding to the ID given.
    """
    for analysis in self.analyses:
      if analysis["ID"] == id_: 
        return analysis
    raise ValueError(f"Analysis ID {id_} not found in file.")
  
  def getAnalysisByName(self, name):
    """
    Return the analysis in the analysis tree corresponding to the name given.
    """
    for analysis in self.analyses:
      if analysis["Name"] == name: 
        return analysis
    raise ValueError(f"Analysis {name} not found in file.")
  
  def getMaterialByName(self, name):
    """
    Return the material corresponding to the name given.
    """
    for mat in self.materials:
      if mat["Name"] == name:
        return mat
    raise ValueError(f"Material {name} not found in file.")
  
  def getMaterialByID(self, id_):
    """
    Return the material corresponding to the ID given.
    """
    for mat in self.materials:
      if mat["ID"] == id_:
        return mat
    raise ValueError(f"Material ID {id_} not found in file.")

  def getReinforcementByName(self, name):
    for x in self.reinforcements:
      if x["Name"] == name:
        return x
    raise ValueError(f"Reinforcement {name} not found in file.")

  def getReinforcementByID(self, id_):
    for x in self.reinforcements:
      if x["ID"] == id_:
        return mat
    raise ValueError(f"Reinforcements ID {id_} not found in file.")
  
  def writeConfigurationFile(self, f_out, prettify=True):
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
    tree = ET.ElementTree(out_root)
    tree.write(f_out, encoding='utf-8', xml_declaration=True, method="xml") 
    if prettify:
      self.__prettifyer__(f_out)
    return
  
  def writeGeoStudioFile(self, f_out, compresslevel=1):
    ext = f_out.split('.')[-1]
    if ext != "gsz":
      f_out += ".gsz"
    prefix = f_out.split('/')[-1][:-4]
    if f_out == self.f_src:
      raise ValueError("Cannot overwriting the source GeoStudio file. Please write within another file.")
    else:
      zip_out = zipfile.ZipFile(
        f_out, mode="w", 
        compression=zipfile.ZIP_DEFLATED, 
        compresslevel=compresslevel
      )
    with zip_out.open(prefix + ".xml", "w") as xml_out:
      self.writeConfigurationFile(xml_out, prettify=False)
    mesh_set = set()
    for geom in self.geometries:
      mesh_set.add(geom.mesh_id)
    for mesh_id in mesh_set:
      if mesh_id is None: continue
      mesh_name = "mesh_" + mesh_id + ".ply"
      zip_out.writestr(mesh_name, data=self.src.read(mesh_name))
    zip_out.close()
    print(f"GeoStudio study successfully written in {f_out}")
    return
  
  def __prettifyer__(self, f_out):
    from bs4 import BeautifulSoup
    with open(f_out, 'r') as src:
      data = '\n'.join(src.readlines())
    bs = BeautifulSoup(data, 'xml')
    data = bs.prettify()
    with open(f_out, 'w') as out:
      out.write(data)
    return
  
  def __eq__(self, other):
    """
    For test purpose
    """
    same = True
    if not self.geometries == other.geometries: 
      same = False
      print("geometries not the same")
    if not self.analyses == other.analysises: 
      same = False
      print("analysis not the same")
    if not self.contexts == other.contexts:
      same = False
      print("contexts not the same")
    if not self.materials == other.materials:
      same = False
      print("materials not the same")
    if not self.f_meshes == other.f_meshes:
      same = False
      print("f_meshes not the same")
    if not self.meshes == other.meshes:
      same = False
      print("meshes not the same")
    return same
    
  
