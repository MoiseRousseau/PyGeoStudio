import xml.etree.ElementTree as ET
import warnings

class BasePropertiesClass:
  """
  This class defined the basic attributes and methods for more specialized
  classes representing for example the material properties, the hydraulic
  function properties and so on.
  """
  def __init__(self, data):
    self.data = data
    self.parameter_type = {}
    return
  
  def __str__(self):
    """
    Print properties of the class
    """
    return self.data.__str__()

  def __write__(self, et):
    """
    Write back the properties in an XML Tree to save the GeoStudio file
    """
    for tag,val in self.data.items():
      if self.parameter_type[tag] is None:
        sub = ET.SubElement(et, tag)
        val.__write__(sub)
        continue
      sub = ET.SubElement(et, tag)
      sub.text = val
    return
  
  def __getitem__(self, parameter):
    """
    Return the property named parameter
    """
    if parameter not in self.data.keys():
      #TODO test if an error is raise, or defined a behavior
      return None
    elif parameter not in self.parameter_type.keys():
      warnings.warn("Property {parameter} defined but not officially handled by PyGeoStudio. Return a properties non-interpreted as a string. Please contact for assistance.", UserWarning)
      return self.data[parameter]
    else:
      if self.parameter_type[parameter] is None:
        return self.data[parameter]
      else:
        return self.parameter_type[parameter](self.data[parameter])
    
  def __setitem__(self, parameter, val):
    """
    Set the property named parameter to the value val (as an string)
    """
    if parameter not in self.data.keys():
      if parameter not in self.parameter_type.keys():
        warnings.warn("Property {parameter} defined in the analysis but not officially handled by PyGeoStudio. Please contact for assistance.", UserWarning)
    if val is True: val = 'true'
    if val is False: val = 'false'
    self.data[parameter] = str(val)
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
