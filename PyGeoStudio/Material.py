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
  :param JointEffectiveCohesion:
  :type JointEffectiveCohesion: float
  :param IntactRockParam:
  :type IntactRockParam: float
  """
  parameter_type = {
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
    "YoungsPrimeModulus" : float,
    "EffectivePoissonsRatio" : float,
    "JointEffectiveCohesion" : float,
    "IntactRockParam" : float,
  }


class MaterialHydraulicFunction(BasePropertiesClass):
  """
  :param KSat: Saturated hydraulic conductivity of the material.
  :type KSat: float
  :param VolWC: Saturated volumic water content
  :type VolWC: float
  :param Beta: Compressibility
  :type Beta: float
  :param KFnNum: Hydraulic conductivity function (for SatUnsat material). Experimental
  :type KFnNum: int
  :param VolWCNum: Water retention curve (for SatUnsat material). Experimental
  :type VolWCNum: int
  """
  parameter_type = {
    # If Sat only
    "KSat":float, #Saturated permeability
    "VolWC":float, #Saturated volumic Water Content (porosity)
    "Beta":float,
    # If non-sat
    "KFnNum":int, #Relative permeability function
    "VolWCNum":int, #Water Retention Curve
  }

  def read(self, et):
    self.data = dict(et.attrib)
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
  parameter_type = {
    "ID" : int,
    "Name" : str,
    "Color" : list,
    "SeepModel" : str,
    "SlopeModel" : str,
    "StressModel" : str,
    "Hydraulic" : MaterialHydraulicFunction,
    "StressStrain" : MaterialStressStrain,
  }

  def __str__(self):
    res = f"Material {self.data['Name']} (ID {self.data['ID']}, RGB color {self.data['Color']})\n"
    res += f"Seep model: {self.data['SeepModel']}\n"
    res += f"Hydraulic Function: {self.data['Hydraulic']}\n"
    res += f"Slope model: {self.data['SlopeModel']}\n"
    res += f"Stress strain model parameter: {self.data['StressStrain']}"
    return res

