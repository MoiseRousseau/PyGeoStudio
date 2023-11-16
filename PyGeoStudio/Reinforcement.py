import xml.etree.ElementTree as ET
from .BasePropertiesClass import BasePropertiesClass
from .Color import Color

class Reinforcement(BasePropertiesClass):
  """
  :param Name: Name of the reinforcement in the GeoStudio study
  :type Name: str
  :param Type: Reinforcement type (Anchors, Pile, Geosynthetic, Nail or UserDefined)
  :type Type: str
  :param ID: index of the reinforcement in the GeoStudio study
  :type ID: float
  :param Color: RGB color (0 to 255) of the material in GeoStudio study.
  :type Color: PyGeoStudio.Color object
  :param ShearForce:
  :type ShearForce: float
  :param ShearReductionFactor:
  :type ShearReductionFactor: float
  :param Spacing:
  :type Spacing: float
  :param BondLength:
  :type BondLength: float
  :param BondDiameter:
  :type BondDiameter: float
  :param PulloutReductionFactor:
  :type PulloutReductionFactor: float
  :param ReinforcementForceReductionFactor:
  :type ReinforcementForceReductionFactor: float
  :param TensileCapacity:
  :type TensileCapacity: float
  :param PulloutResistance:
  :type PulloutResistance: float
  :param ForceDistribution:
  :type ForceDistribution: float
  :param FofSDependent:
  :type FofSDependent: bool
  :param CalculatedPulloutResistance:
  :type CalculatedPulloutResistance: bool
  :param SurfaceAreaFactor:
  :type SurfaceAreaFactor: float
  :param ReinfForceVsDistanceFnNum: User defined function of the reinforcements
  :type ReinfForceVsDistanceFnNum: int
  :param ForceOrientation:
  :type ForceOrientation: float
  """
  def __init__(self, data):
    self.data = data
    self.parameter_type = {
      "Name" : str, 
      "Type" : str, #Must be Anchors, Pile, Geosynthetic, Nail, UserDefined (seems to be Anchors by default)
      "ID" : int,
      "Color" : Color,
      "ShearForce" : float, #Pile, Anchors
      "ShearReductionFactor" : float, #Pile, Anchors
      "Spacing" : float, #Anchors, Nail
      "BondLength" : float, #Anchors
      "BondDiameter" : float, #Anchors, Nail
      "PulloutReductionFactor" : float, #Anchors, Geosynthetic, Nail
      "ReinforcementForceReductionFactor" : float, #Anchors, Geosynthetic, Nail, UserDefined
      "TensileCapacity" : float, #Anchors, Geosynthetic, Nail
      "PulloutResistance" : float, #Anchors, Geosynthetic, Nail
      "ForceDistribution" : str, #Anchors, UserDefined
      "FofSDependent" : bool, #Geosynthetic, Nail, UserDefined
      "CalculatedPulloutResistance" : bool, #Geosynthetic
      "SurfaceAreaFactor" : float, #Geosynthetic
      "ReinfForceVsDistanceFnNum" : int, #UserDefined
      "ForceOrientation" : float, #UserDefined
    }
    return
