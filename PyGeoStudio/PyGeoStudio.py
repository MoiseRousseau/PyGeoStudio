import plyfile
import zipfile
import os
import numpy as np
import xml.etree.ElementTree as ET

from PyGeoStudio.GeoAnalysis import GeoStudioAnalysis 
from PyGeoStudio.GeoGeometry import GeoStudioGeometry 
from PyGeoStudio.GeoContext import GeoStudioContext
from PyGeoStudio.GeoMaterial import GeoStudioMaterial

class GeoStudioFile:
  def __init__(self, geostudio_file, mode='r'):
    self.f_src = geostudio_file
    self.open_mode = mode
    
    self.geometries = []
    self.analysises = []
    self.contexts = []
    self.materials = []
    self.f_meshes = []
    self.meshes = []
    self.unsupported_items = []
    self.initialize()
    return
    
  def showAnalysisTree_old(self):
    #get folder
    file_list = self.src.namelist()
    folders = list(set(x.split('/')[0] for x in file_list if len(x.split('/'))>1))
    folders.sort()
    #print it
    print(f"GeoStudio file: {self.f_src}")
    i = 0
    while i<len(folders):
      x = folders[i]
      print(f"  | {x}")
      if 0: #(i != len(folders)-1) and (x in folders[i+1]):
        i += 1
        subfolder = folders[i]
        while x in subfolder:
          print(f"    | {subfolder}")
          i += 1
          subfolder = folders[i]
      else:
        i += 1
    return
  
  def showAnalysisTree(self, detail_level=0):
    print(f"GeoStudio file: {self.f_src}")
    #first pass, those with no parentID
    for analysis in self.analysises:
      print(analysis.ID, analysis.Name)
    return
  
  def getMeshVertices(self):
    """
    Return a numpy array of the mesh vertices
    """
    print("how to choose the right mesh?")
    return
    data = self.src_mesh.elements[1].data
    return np.array((data['x'], data['y'], data['z'])).transpose()
  
  def getMeshElement(self):
    #TODO
    print("Moise: I still need to understand how mesh connectivity is stored")
    return None
  
  def initialize(self):
    #open file
    if os.path.isfile(self.f_src):
      self.src = zipfile.ZipFile(self.f_src, self.open_mode)
    else:
      print(f"File {self.f_src} doesn't exist in the current directory")
      raise ValueError
    #parse geoslope input
    self.main_xml = ET.parse(self.src.open(self.f_src[:-3]+'xml'))
    root = self.main_xml.getroot()
    for element in root:
      #print(element.tag)
      if element.tag == "FileInfo":
        self.f_src_info = element.attrib
      elif element.tag == "Geometries":
        self.__readGeometry__(element)
      elif element.tag == "Analyses":
        self.__readAnalysis__(element)
      elif element.tag == "Contexts":
        #context define the material properties associated with the analysis and BC
        self.__readContexts__(element)
      elif element.tag == "Materials":
        self.__readMaterials__(element)
      else:
        #store the item for the write method
        self.unsupported_items.append(element)
    
    for mesh in self.f_meshes:
      self.meshes.append(self.src.read(mesh))
    
    return
    
  def __readGeometry__(self,element):
    self.n_geometry = int(element.attrib["Len"])
    for i in range(self.n_geometry):
      new_geom = GeoStudioGeometry(self.src)
      new_geom.read(element[i])
      self.f_meshes.append("mesh_"+new_geom.mesh_id+".ply")
      self.geometries.append(new_geom)
    return
  
  def __readAnalysis__(self,element):
    self.n_analysis = int(element.attrib["Len"])
    for i in range(self.n_analysis):
      new_analysis = GeoStudioAnalysis(self.src)
      new_analysis.Index_in_xml = i
      for property_ in element[i]:
        try:
          setattr(new_analysis, property_.tag, property_.text)
        except:
          print(property_.tag)
      self.analysises.append(new_analysis)
    return
  
  def __readContexts__(self, element):
    self.n_contexts = int(element.attrib["Len"])
    for i in range(self.n_contexts):
      new_context = GeoStudioContext(self.src)
      new_context.read(element[i])
      self.contexts.append(new_context)
    return
  
  def __readMaterials__(self, element):
    self.n_materials = int(element.attrib["Len"])
    for i in range(self.n_materials):
      mat_ = element[i]
      new_mat = GeoStudioMaterial(self.src)
      new_mat.read(mat_)
      self.materials.append(new_mat)
      
  
  def getGeometry(self, id_):
    return self.geometries[id_-1]
  
  def __getitem__(self, key):
    for analysis in self.analysises:
      if analysis.Name == key: 
        analysis.__initiate__()
        analysis.defineGeometry(self.getGeometry(analysis.GeometryId))
        for context in self.contexts:
          if context.analysisID == analysis.ID:
            break
        analysis.defineContext(context)
        return analysis
    print(f"Analysis {key} not found in file.")
    raise ValueError
  
  def getAnalysis(self, key):
    for analysis in self.analysises:
      if analysis.Name == key: 
        analysis.__initiate__()
        return analysis
    print(f"Analysis {key} not found in file.")
    raise ValueError
  
  def getAllAnalysis(self):
    return self.analysises
  
  def getMaterialByName(self, name):
    for mat in self.materials:
      if mat.name == name:
        return mat
    print(f"Material {name} not found in file.")
    raise ValueError
  
  def getMaterials(self):
    return self.materials
  
  def getMaterialByID(self, id):
    for mat in self.materials:
      if mat.id == id:
        return mat
    print(f"Material ID {name} not found in file.")
    raise ValueError
  
  def writeAnalysis(self, out):
    
    return
  
