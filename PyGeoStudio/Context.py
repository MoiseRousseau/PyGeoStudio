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

import numpy as np
import xml.etree.ElementTree as ET
import warnings

from .BasePropertiesClass import BasePropertiesClass


class Context(BasePropertiesClass):
  """
  :param AnalysisID: ID of the analysis to apply this context. Handle automatically by PyGeoStudio. Do not change until you know what you are doing.
  :type AnalysisID: int
  :param GeometryUsesMaterials: Material distribution as a dictionnary such as ``{"region_name_1" : mat_id_1, "region_name_2" : mat_id_2, ...}``
  :type GeometryUsesMaterials: dict
  :param HydraulicBCDistribution: Distribution of the hydraulic boundary condition as a dictionnary such as ``{}``
  :type HydraulicBCDistribution: dict
  """
  parameter_type = {
    "AnalysisID" : int,
    "GeometryUsesMaterials" : dict,
    "HydraulicBCDistribution" : dict,
  }
  my_data = []

  def read(self, element):
    """
    :meta private:
    """
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
