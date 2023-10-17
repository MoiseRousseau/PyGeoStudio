import xml.etree.ElementTree as ET
from .BasePropertiesClass import BasePropertiesClass

class MaterialStressStrain(BasePropertiesClass):
  def __init__(self, data):
    self.data = data
    self.parameter_type = {
      "ResponseType" : str,
      "UnitWeight" : float, 
      "CohesionPrime" : float,
      "PhiPrime" : float,
      "Rf" : float, 
      "OCRatio" : float,
      "ConsolLambda" : float,
      "OCKappa" : float,
      "InitVoidRatio" : float,
      "YieldSurfaceShape" : float,
      "LimitOfAnisotropy" : float,
    }
    return


class MaterialHydraulicFunction(BasePropertiesClass):
  """
  Defined a hydraulic function.
  Note the properties are defined as an attribute in GeoStudio file, so a custom __write__ function is needed.
  """
  def __init__(self, data):
    print(data)
    self.data = data
    self.parameter_type = {
      # If Sat only
      "KSat":float, #Saturated permeability
      "VolWC":float, #Volumic Water Content (porosity)
      "Beta":float,
      # If non-sat
      "KFnNum":int, #Relative permeability function
      "VolWCNum":int, #Water Retention Curve
    }
    return
  
  def __write__(self, et):
    """
    Custom write function to write properties as an attribute.
    """
    sub = ET.SubElement(et, "Hydraulic")
    sub.attrib = {x:y for x,y in self.data.items()}
    return


class Material:
  def __init__(self):
    self.mat_data = {}
    self.parameter_type = {
      "ID" : int,
      "Name" : str, 
      "Color" : list,
      "SeepModel" : str,
      "SlopeModel" : float, 
      "Hydraulic" : None, #None means another XML Tree
      "StressStrain" : None,
    }
    return
  
  def __str__(self):
    res = f"Material {self.mat_data['Name']} (ID {self.mat_data['ID']}, RGB color {self.mat_data['Color']})\n"
    res += f"Seep model: {self.mat_data['SeepModel']}\n"
    res += f"Hydraulic Function: {self.mat_data['Hydraulic']}\n"
    res += f"Slope model: {self.mat_data['SlopeModel']}\n"
    res += f"Stress strain model parameter: {self.mat_data['StressStrain']}"
    return res
  
  def properties(self):
    """
    Show the available reinforcement object properties that is interfaced through PyGeoStudio
    """
    return self.mat_data
  
  def availableProperties(self):
    """
    Show the available reinforcement object properties that is interfaced through PyGeoStudio
    """
    return list(self.parameter_type.keys())
  
  def read(self, reinf_):
    """
    Read material information contained in XML tree under Material
    """
    for prop in reinf_:
      if prop.tag == "StressStrain":
        self.mat_data["StressStrain"] = MaterialStressStrain({x.tag:x.text for x in prop})
      elif prop.tag == "Hydraulic":
        self.mat_data["Hydraulic"] = MaterialHydraulicFunction(prop.attrib)
      else:
        self.mat_data[prop.tag] = prop.text
    return
  
  def __getitem__(self, parameter):
    if parameter not in self.mat_data.keys():
      return None
    elif parameter not in self.parameter_type.keys():
      warnings.warn("Property {parameter} defined in the material but not officially handled by PyGeoStudio. Return a properties non-interpreted as a string. Please contact for assistance.", UserWarning)
      return self.mat_data[parameter]
    else:
      if self.parameter_type[parameter] is None:
        return self.mat_data[parameter]
      else:
        return self.parameter_type[parameter](self.mat_data[parameter])
  
  def __setitem__(self, parameter, val):
    if parameter not in self.mat_data.keys():
      if parameter not in self.parameter_type.keys():
        warnings.warn("Parameter {parameter} defined in the analysis but not officially handled by PyGeoStudio. Please contact for assistance.", UserWarning)
    if val is True: val = 'true'
    if val is False: val = 'false'
    self.mat_data[parameter] = str(val)
    return
  
  def write(self, et):
    for tag,val in self.mat_data.items():
      if self.parameter_type[tag] is None:
        val.__write__(et)
        continue
      sub = ET.SubElement(et, tag)
      sub.text = val
    return
  
  def __eq__(self, other):
    if type(other) != type(other):
      return False
    if len(self.mat_data) != len(other.mat_data):
      return False
    for prop,val in self.mat_data:
      if other.mat_data[prop] != val:
         return False
    return True
