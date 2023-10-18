import xml.etree.ElementTree as ET
from .BasePropertiesClass import BasePropertiesClass

class Reinforcement(BasePropertiesClass):
  def __init__(self, data):
    self.data = data
    self.parameter_type = {
      "Name" : str, 
      "Type" : str, #Must be Pile, Geosynthetic, Nail, UserDefined (seems to be Anchors by default)
      "ID" : int,
      "Color" : list,
      "ShearForce" : float, #Pile
      "ShearReductionFactor" : float, #Pile
      "Spacing" : float, #Anchors, Nail
      "BondLength" : float, #Anchors
      "BondDiameter" : float, #Anchors, Nail
      "PulloutReductionFactor" : float, #Anchors, Geosynthetic, Nail
      "ReinforcementForceReductionFactor" : float, #Anchors, Geosynthetic, Nail, UserDefined
      "TensileCapacity" : float, #Anchors, Geosynthetic, Nail
      "PulloutResistance" : float, #Anchors, Geosynthetic, Nail
      "ForceDistribution" : str, #Anchors, UserDefined
      "ShearForce" : float, #Anchors
      "ShearReductionFactor" : float, #Anchors
      "FofSDependent" : bool, #Geosynthetic, Nail, UserDefined
      "CalculatedPulloutResistance" : bool, #Geosynthetic
      "CalculatedPulloutResistance" : bool, #Geosynthetic
      "SurfaceAreaFactor" : float, #Geosynthetic
      "ReinfForceVsDistanceFnNum" : int, #UserDefined
      "ForceOrientation" : float, #UserDefined
    }
    return
