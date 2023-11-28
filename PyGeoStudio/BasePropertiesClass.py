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

import xml.etree.ElementTree as ET
import warnings

class BasePropertiesClass:
  """
  This class defined the basic attributes and methods for more specialized
  classes representing for example the material properties, the hydraulic
  function properties and so on.
  
  Contains two structures:
  * data: data is a dictionnary that contains all the properties the user can access in PyGeoStudio
  * parameter_type: explicitely define the type of the properties to interact with in Python
  * my_data: list of properties only defined in PyGeoStudio for more intuitive interfacing

  In parameter_type, if the value is dict, it is written as a attrib
  """
  parameter_type = {}
  my_data = []
  def __init__(self, prop):
    self.data = {}
    self.other_elem = []
    self.read(prop)
    return

  def __str__(self):
    """
    Print properties of the class
    """
    return self.data.__str__()

  def __setitem__(self, property_, val):
    """
    Set the property named property_ to the value val.
    """
    if val is True: val = 'true'
    if val is False: val = 'false'
    if property_ in self.my_data: #do not interpret the property defined in my_data
      self.data[property_] = val
      return
    if property_ not in self.data.keys():
      if property_ not in self.parameter_type.keys():
        raise ValueError(f"Property {property_} not defined in PyGeoStudio. If you feel this is an error, please contact for assistance.")
    self.data[property_] = str(val)
    return

  def __getitem__(self, property_):
    """
    Return the property.
    """
    if property_ in self.data.keys(): #return to the user
      if property_ in self.parameter_type.keys(): # already seen and handled but PyGeoStudio
        func = self.parameter_type[property_]
        if func in [dict, int, str, float, bool]: #Convert to standard Python object
          return func(self.data[property_])
        else: #returned the PyGeoStudio object
          return self.data[property_]
      else: #not handled
        warnings.warn(f"Property {property_} defined but not officially handled by PyGeoStudio.\nReturn property non-interpreted as a string. Please contact for assistance.", UserWarning)
        return self.data[property_]
    elif property_ in self.parameter_type.keys(): #not defined in the analysis but PyGeoStudio knows it
      return None
    elif property_ in [x.tag for x in self.other_elem]:
      warnings.warn(f"Property named \"{property_}\" defined, but it has a complex structure not yet handled by PyGeoStudio. Return it as a raw XML tree. Good luck or please contact for assistance.")
      for x in self.other_elem:
        if x.tag == property_: return x
    else: #totally unknown
      raise ValueError(f"Property named \"{property_}\" not defined in the file, neither handled by PyGeoStudio. If you feel this is an error, please contact for assistance.")

  def read(self, et):
    """
    Read the XML element tree and populate the class. The rules:
    1. If the property is Missing, skip it
    2. If the property is a subtree not known / handled by PyGeoStudio, store it as is
    3. If the property is interpreted as a dict, take the attribute
    4. If the property is interpreted as a list, parse the list
    5. If a custom class stores the property, call the constructor
    6. Parse property as a string
    """
    for prop in et:
      prop_type = self.parameter_type.get(prop.tag)
      # 1
      if prop.attrib.get("Missing") == "true": 
        continue
      # 2
      elif len(prop) > 0 and prop_type is None: 
        self.other_elem.append(prop)
      # 3
      elif prop_type is dict: 
        self.data[prop.tag] = prop.attrib
      # 4
      elif prop_type is list:
        self.data[prop.tag] = []
        for d in prop:
          v = [d.tag, d.attrib]
          self.data[prop.tag].append(v)
      # 5
      elif "PyGeoStudio" in str(prop_type):
        self.data[prop.tag] = self.parameter_type[prop.tag](prop)
      # 6
      elif len(prop) == 0:
        self.data[prop.tag] = prop.text
      else:
        raise ValueError("You are not supposed to be here...")

    #custom method to set other property
    self.__initialize__()
    return

  def __write__(self, et):
    """
    Write back the properties in an XML Tree to save the GeoStudio file
    """
    self.__deinitialize__()
    for tag,val in self.data.items():
      if tag in self.my_data: continue #skip property defined in this lib
      prop_type = self.parameter_type.get(tag)
      if "PyGeoStudio" in str(prop_type):
        sub = ET.SubElement(et, tag)
        val.__write__(sub)
        continue
      sub = ET.SubElement(et, tag)
      if isinstance(val, dict):
        sub.attrib = val
        continue
      if isinstance(val, list):
        sub.attrib = {"Len":str(len(val))}
        for v in val:
          item = ET.SubElement(sub, v[0])
          item.attrib = v[1]
        continue
      if not isinstance(val, str):
        raise ValueError(f"Can't write property {tag} because value is not a string: {val}")
      sub.text = val
    for prop in self.other_elem:
      et.append(prop)
    self.__initialize__()
    return

  def __initialize__(self):
    """
    Post process some attribute
    """
    return

  def __deinitialize__(self):
    """
    De-process some attribute for the write method
    """
    return

  def getAllProperties(self):
    """
    Return a dictionnary holding all the properties of the class.
    Note: you should know what to do when changing manually these properties.
    """
    return self.data

  def showAvailableProperties(self):
    """
    Show the available object properties that is interfaced through PyGeoStudio
    """
    return self.parameter_type.keys()
