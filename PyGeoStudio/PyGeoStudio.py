import plyfile
import zipfile
import os
import numpy as np
import xml.etree.ElementTree as ET

from PyGeoStudio.GeoAnalysis import GeoStudioAnalysis 
from PyGeoStudio.GeoGeometry import GeoStudioGeometry 
from PyGeoStudio.GeoContext import GeoStudioContext

class GeoStudioFile:
  def __init__(self, geostudio_file, mode='r'):
    self.f_src = geostudio_file
    self.open_mode = mode
    
    self.geometries = []
    self.analysises = []
    self.contexts = []
    self.f_meshes = []
    self.meshes = []
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
      if element.tag == "Geometries":
        self.__readGeometry__(element)
      if element.tag == "Analyses":
        self.__readAnalysis__(element)
      if element.tag == "Contexts":
        self.__readContexts__(element)
    
    for mesh in self.f_meshes:
      self.meshes.append(self.src.read(mesh))
    
    return
    
  def __readGeometry__(self,element):
    self.n_geometry = int(element.attrib["Len"])
    for i in range(self.n_geometry):
      new_geom = GeoStudioGeometry(self.src)
      for property_ in element[i]:
        if property_.tag == "Points":
          new_geom.points = np.zeros((int(property_.attrib["Len"]),2),dtype='f8')
          for point in property_:
            new_geom.points[int(point.attrib["ID"])-1] = [float(point.attrib["X"]), float(point.attrib["Y"])]
        elif property_.tag == "Lines":
          new_geom.lines = np.zeros((int(property_.attrib["Len"]),2),dtype='i8')-1
          for line in property_:
            new_geom.lines[int(line[0].text)-1] = [int(line[1].text)-1,int(line[2].text)-1]
        elif property_.tag == "Regions":
          new_geom.regions = np.zeros((int(property_.attrib["Len"]),99),dtype='i8')-1
          for region in property_:
            id_ = int(region[0].text)-1
            pts = [int(x)-1 for x in region[1].text.split(',')]
            pts += [-1 for x in range(99-len(pts))]
            new_geom.regions[int(region[0].text)-1] = pts
        elif property_.tag == "MeshId":
          self.f_meshes.append("mesh_"+property_.text+".ply")
          setattr(new_geom, property_.tag, property_.text)
        else:
          setattr(new_geom, property_.tag, property_.text)
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
      for property_ in element[i]:
        if property_.tag == "GeometryUsesMaterials":
          new_context.material_distribution = np.zeros((int(property_.attrib["Len"]),2), dtype='i8')-1
          for i,mat in enumerate(property_):
            reg = int(mat.attrib["ID"].split('-')[-1])
            mat_id = int(mat.attrib["Entry"])
            new_context.material_distribution[i] = [reg,mat_id]
        if property_.tag == "AnalysisID":
          new_context.analysisID = int(property_.text)
      self.contexts.append(new_context)
    return
  
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
