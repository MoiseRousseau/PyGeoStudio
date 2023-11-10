import numpy as np
import xml.etree.ElementTree as ET
import warnings

from .BasePropertiesClass import BasePropertiesClass


class Context(BasePropertiesClass):
  """
  Context class couples analyses with the material distribution and boundary conditions
  """
  def __init__(self, data={}):
    self.data = data
    self.parameter_type = {
      "AnalysisID" : int,
      "GeometryUsesMaterials" : dict,
      "HydraulicBCDistribution" : dict,
    }
    self.my_data = []
    return
  
  def read(self, element):
    for property_ in element:
      if property_.tag == "GeometryUsesMaterials":
        n = int(property_.attrib["Len"])
        if "GeometryUsesMaterials" not in self.data.keys(): self.data["GeometryUsesMaterials"] = {}
        for i,mat in enumerate(property_):
          reg = mat.attrib["ID"]
          mat_id = int(mat.attrib["Entry"])
          self.data["GeometryUsesMaterials"][reg] = mat_id
        if len(self.data["GeometryUsesMaterials"]) != n:
          warnings.warn("Number of GeometryUsesMaterials defined in the input GeoStudio file does not match what was read. This is probably an error in your GeoStudio file")
      elif property_.tag == "GeometryUsesHydraulicBCs":
        n = int(property_.attrib["Len"])
        if "GeometryUsesHydraulicBCs" not in self.data.keys(): self.data["GeometryUsesHydraulicBCs"] = {}
        for i,mat in enumerate(property_):
          reg = mat.attrib["ID"]
          mat_id = int(mat.attrib["Entry"])
          self.data["GeometryUsesHydraulicBCs"][reg] = mat_id
        if len(self.data["GeometryUsesHydraulicBCs"]) != n:
          warnings.warn("Number of GeometryUsesHydraulicBCs defined in the input GeoStudio file does not match what was read. This is probably an error in your GeoStudio file")
      else:
        self.data[property_.tag] = property_.text
    return
  
  def __write__(self, et):
    #analysis ID
    for tag,val in self.data.items():
      match tag:
        case "GeometryUsesMaterials":
          sub = ET.SubElement(et, tag)
          sub.attrib = {"Len" : str(len(self.data[tag]))}
          for reg, mat_id in self.data["GeometryUsesMaterials"].items():
            sub_gum = ET.SubElement(sub, "GeometryUsesMaterial")
            sub_gum.attrib["ID"] = reg
            sub_gum.attrib["Entry"] = str(mat_id)
        case "GeometryUsesHydraulicBCs":
          sub = ET.SubElement(et, tag)
          sub.attrib = {"Len" : str(len(self.data[tag]))}
          for reg, mat_id in self.data["GeometryUsesHydraulicBCs"].items():
            sub_gum = ET.SubElement(sub, "GeometryUsesHydraulicBCs")
            sub_gum.attrib["ID"] = reg
            sub_gum.attrib["Entry"] = str(mat_id)
        case _:
          sub = ET.SubElement(et, tag)
          sub.text = val
    return
