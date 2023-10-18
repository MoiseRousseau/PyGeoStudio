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
  
  def __write__(self, sub):
    """
    Custom write function to write properties as an attribute.
    """
    sub.attrib = {x:y for x,y in self.data.items()}
    return


class Material(BasePropertiesClass):
  def __init__(self):
    self.data = {}
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
    res = f"Material {self.data['Name']} (ID {self.data['ID']}, RGB color {self.data['Color']})\n"
    res += f"Seep model: {self.data['SeepModel']}\n"
    res += f"Hydraulic Function: {self.data['Hydraulic']}\n"
    res += f"Slope model: {self.data['SlopeModel']}\n"
    res += f"Stress strain model parameter: {self.data['StressStrain']}"
    return res
  
  def read(self, reinf_):
    """
    Read material information contained in XML tree under Material
    """
    for prop in reinf_:
      if prop.tag == "StressStrain":
        self.data["StressStrain"] = MaterialStressStrain({x.tag:x.text for x in prop})
      elif prop.tag == "Hydraulic":
        self.data["Hydraulic"] = MaterialHydraulicFunction(prop.attrib)
      else:
        self.data[prop.tag] = prop.text
    return
  
  def __eq__(self, other):
    if type(other) != type(other):
      return False
    if len(self.data) != len(other.data):
      return False
    for prop,val in self.data:
      if other.data[prop] != val:
         return False
    return True
