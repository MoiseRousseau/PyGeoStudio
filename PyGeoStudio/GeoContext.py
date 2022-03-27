import numpy as np
import xml.etree.ElementTree as ET

class GeoStudioContext:
  def __init__(self):
    self.material_distribution = {}
    self.hydraulic_bc_distribution = {}
    self.analysisID = -1
    self.other_elem = []
    return
  
  def __str__(self):
    return 
  
  def read(self, element):
    for property_ in element:
      if property_.tag == "GeometryUsesMaterials":
        n = int(property_.attrib["Len"])
        for i,mat in enumerate(property_):
          reg = mat.attrib["ID"]
          mat_id = int(mat.attrib["Entry"])
          self.material_distribution[reg] = mat_id
        if len(self.material_distribution) != n:
          print("Warning, error reading \"GeometryUsesMaterials\"")
      elif property_.tag == "GeometryUsesHydraulicBCs":
        n = int(property_.attrib["Len"])
        for i,mat in enumerate(property_):
          reg = mat.attrib["ID"]
          mat_id = int(mat.attrib["Entry"])
          self.hydraulic_bc_distribution[reg] = mat_id
        if len(self.hydraulic_bc_distribution) != n:
          print("Warning, error reading \"GeometryUsesHydraulicBCs\"")
      elif property_.tag == "AnalysisID":
        self.analysisID = int(property_.text)
      else:
        self.other_elem.append(property_)
    return
  
  def write(self, et):
    #analysis ID
    sub = ET.SubElement(et, "AnalysisID")
    sub.text = str(self.analysisID)
    #geom use mat
    if self.material_distribution:
      sub = ET.SubElement(et, "GeometryUsesMaterials")
      sub.attrib = {"Len":str(len(self.material_distribution))}
      for reg, mat_id in self.material_distribution.items():
        sub_gum = ET.SubElement(sub, "GeometryUsesMaterial")
        sub_gum.attrib["ID"] = reg
        sub_gum.attrib["Entry"] = str(mat_id)
    #geom use BC
    if self.hydraulic_bc_distribution:
      sub = ET.SubElement(et, "GeometryUsesHydraulicBCs")
      sub.attrib = {"Len":str(len(self.hydraulic_bc_distribution))}
      for reg, mat_id in self.material_distribution.items():
        sub_gum = ET.SubElement(sub, "GeometryUsesHydraulicBC")
        sub_gum.attrib["ID"] = reg
        sub_gum.attrib["Entry"] = str(mat_id)
    #others
    for prop in self.other_elem:
      et.append(prop)
    return
  
  def __eq__(self, other):
    print(f"-----------------------\nTest context")
    same = True
    if self.material_distribution != other.material_distribution: same = False
    if self.hydraulic_bc_distribution != other.hydraulic_bc_distribution: same = False
    if self.analysisID != other.analysisID: same = False
    return same
