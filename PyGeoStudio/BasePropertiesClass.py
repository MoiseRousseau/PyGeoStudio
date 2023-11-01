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
  data = {}
  parameter_type = {} #data from the GeoStudio file
  my_data = []

  def __init__(self, data):
    self.data = data
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
        if func is None:
          return self.data[property_]
        else:
          return func(self.data[property_])
      else: #not handled
        warnings.warn(f"Property {parameter} defined but not officially handled by PyGeoStudio.\nReturn property non-interpreted as a string. Please contact for assistance.", UserWarning)
        return self.data[property_]
    elif property_ in self.parameter_type.keys(): #not defined in the analysis but PyGeoStudio knows it
      return None
    else: #totally unknown
      raise ValueError(f"Property named \"{property_}\" not defined in the file, neither handled by PyGeoStudio. If you feel this is an error, please contact for assistance.")

  def read(self, et):
    """
    Read the XML element tree and populate the class
    """
    for prop in et:
      self.data[prop.tag] = prop.text
    return

  def __write__(self, et):
    """
    Write back the properties in an XML Tree to save the GeoStudio file
    """
    for tag,val in self.data.items():
      if tag in self.my_data: continue #skip property defined in this lib
      if self.parameter_type.get(tag, 1) is None:
        sub = ET.SubElement(et, tag)
        val.__write__(sub)
        continue
      sub = ET.SubElement(et, tag)
      if isinstance(val, dict):
        sub.attrib = val
        continue
      if not isinstance(val, str):
        raise ValueError(f"Can't write property {tag} because value is not a string: {val}")
      sub.text = val
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
