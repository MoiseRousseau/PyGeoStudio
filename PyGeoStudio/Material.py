import xml.etree.ElementTree as ET
from .BasePropertiesClass import BasePropertiesClass

class MaterialStressStrain(BasePropertiesClass):
  """
  :param ResidualWCPercent:
  :type ResidualWCPercent: float
  :param GeologicalStrengthIndex:
  :type GeologicalStrengthIndex: float
  :param ResponseType:
  :type ResponseType: str
  :param UnitWeight:
  :type UnitWeight: float
  :param CohesionPrime:
  :type CohesionPrime: float
  :param PhiPrime:
  :type PhiPrime: float
  :param Rf:
  :type Rf: float
  :param OCRatio:
  :type OCRatio: float
  :param ConsolLambda:
  :type ConsolLambda: float
  :param OCKappa:
  :type OCKappa: float
  :param InitVoidRatio:
  :type InitVoidRatio: float
  :param YieldSurfaceShape:
  :type YieldSurfaceShape: float
  :param LimitOfAnisotropy:
  :type LimitOfAnisotropy: float
  :param YoungsPrimeModulus: Young modulus in SIGMA analysis
  :type YoungsPrimeModulus: float
  :param EffectivePoissonsRatio: Poisson ratio in SIGMA analysis
  :type EffectivePoissonsRatio: float
  """
  def __init__(self, data):
    self.data = data
    self.parameter_type = {
      "ResidualWCPercent" : float,
      "GeologicalStrengthIndex" : float,
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
  :param KSat: Saturated hydraulic conductivity of the material.
  :type KSat: float
  :param VolWC: Volumic water content (porosity)
  :type VolWC: float
  :param Beta:
  :type Beta: float
  :param KFnNum: Hydraulic conductivity function (for SatUnsat material). Experimental
  :type KFnNum: int
  :param VolWCNum: Water retention curve (for SatUnsat material). Experimental
  :type VolWCNum: int
  """
  def __init__(self, data):
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
  """  
  :param ID: ID of the material in GeoStudio file. Do not change this property unless you know what your are doing
  :type ID: int
  :param Name: Name of the material in GeoStudio study.
  :type Name: str
  :param Color: RGB color (0 to 255) of the material in GeoStudio study.
  :type Color: [int, int, int]
  :param SeepModel: Hydraulic model in SEEP ("SatOnly" for saturated model only or "SatUnsat" for variably saturated model).
  :type SeepModel: str
  :param SlopeModel: Geomechanical model in SLOPE (MohrCoulomb, ...)
  :type SlopeModel: str
  :param StressModel: Geomechanical model in SIGMA (LinearElastric, ...)
  :type StressModel: str
  :param Hydraulic: Hydraulic properties of the material. This is an instance of MaterialHydraulicFunction class.
  :type Hydraulic: MaterialHydraulicFunction object
  :param StressStrain: Geotechnical properties of the material. This is an instance of MaterialStressStrain class.
  :type StressStrain: MaterialStressStrain object
  """
  def __init__(self):
    self.data = {}
    self.parameter_type = {
      "ID" : int,
      "Name" : str, 
      "Color" : list,
      "SeepModel" : str,
      "SlopeModel" : str,
      "StressModel" : str,
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
  
  def read(self, mat_):
    """
    Read material information contained in XML tree under Material
    
    :meta private:
    """
    for prop in mat_:
      if prop.tag == "StressStrain":
        x = MaterialStressStrain({})
        x.read(prop)
        self.data["StressStrain"] = x
      elif prop.tag == "Hydraulic":
        self.data["Hydraulic"] = MaterialHydraulicFunction(prop.attrib)
      else:
        self.data[prop.tag] = prop.text
    return

