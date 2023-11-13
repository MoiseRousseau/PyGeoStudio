import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

from .BasePropertiesClass import BasePropertiesClass


# Note in the GeoStudioFile, material distribution / BC are defined through a Context element.
# We add it in this class because their is one context per analysis...


class TimeIncrements(BasePropertiesClass):
  """
  TimeIncrement holds the time for which the simulation results must be saved
  """
  def __init__(self, data):
    self.data = data
    self.parameter_type = {
      "Duration" : float, #total duration of the simulation
      "IncrementOption" : str, #Exponential
      "IncrementCount" : int,
      "InitialIncrementSize" : float,
      "TimeSteps" : list,
    }
    return
  
  def read(self, et):
    """
    Read the XML element tree and populate the class
    """
    for prop in et:
      if prop.tag == "TimeSteps":
        if "TimeSteps" not in self.data.keys(): self.data["TimeSteps"] = []
        n = int(prop.attrib["Len"])
        for i,time in enumerate(prop):
          self.data["TimeSteps"].append(dict(time.attrib))
      else:
        self.data[prop.tag] = prop.text
    return
  
  def __write__(self, et):
    for tag,val in self.data.items():
      if tag == "TimeSteps":
        sub = ET.SubElement(et, tag)
        sub.attrib = {"Len" : str(len(self.data[tag]))}
        for time in self.data["TimeSteps"]:
          sub_time = ET.SubElement(sub, "TimeStep")
          sub_time.attrib = time
        continue
      if tag in self.parameter_type.keys() and self.parameter_type[tag] is None:
        sub = ET.SubElement(et, tag)
        val.__write__(sub)
        continue
      sub = ET.SubElement(et, tag)
      sub.text = val
    return
  
  def getSavedTimeStep(self):
    return [x["ElapsedTime"] for x in self.data["TimeSteps"] if x["Save"]]


class Analysis(BasePropertiesClass):
  """
  :param ID: Index of the analysis in GeoStudio file
  :type ID: int
  :param Name: Name of the analysis in GeoStudio file
  :type Name: str
  :param Kind: Type of analysis (SEEP or SLOPE)
  :type Kind: str
  :param Description: More information about the analysis
  :type Description: str
  :param ParentID: Index of the parent analysis in GeoStudio file
  :type ParentID: int
  :param Method:
  :type Method: str
  :param GeometryId: Index of the Geometry of the analysis in GeoStudio file. Handle automatically by PyGeoStudio. Do not change until you know what you are doing.
  :type GeometryId: str
  :param Geometry: Geometry of the analysis. Use the method ``setGeometry()`` below to change this property.
  :type Geometry: Geometry object
  :param Context: Boundary condition and material distribution coupler. Use the method ``setContext()`` below to change this property.
  :type Context: Context object
  :param ExcludeInitDeformation:
  :type ExcludeInitDeformation: bool
  :param Results: Interface to analysis results
  :type Results: Results object
  :param TimeIncrements: Timestepping control 
  :type TimeIncrements: TimeIncrements object
  :param ComputedPhysics:
  :type ComputedPhysics: dict
  """
  def __init__(self, data):
    self.data = data
    self.parameter_type = {
      "ID" : int,
      "Name" : str,
      "Kind" : str,
      "Description": str,
      "ParentID" : int,
      "Method" : str,
      "GeometryId" : int,
      "Geometry" : None,
      "Context" : None,
      "ExcludeInitDeformation" : bool,
      "Results": None,
      "TimeIncrements" : None,
      "ComputedPhysics" : dict,
       #TODO below
#      "ConvergenceCriteria" : None,
#      "IterationControls" : None,
#      "UnderRelaxationCriteria" : None,
    }
    self.my_data = ["Geometry", "Context", "Results"]
    return
  
  def __repr__(self):
    res = f"<PyGeoStudio.Analysis object, (ID: {self.data['ID']}, Name: \"{self.data['Name']}\")>"
    return res
  
  def read(self,et):
    """
    :meta private:
    """
    for prop in et:
      match prop.tag:
        case "TimeIncrements":
          timeinc = TimeIncrements({})
          timeinc.read(prop)
          self.data["TimeIncrements"] = timeinc
        case "ComputedPhysics":
          self.data["ComputedPhysics"] = prop.attrib
        case _:
          self.data[prop.tag] = prop.text
  
  def setGeometry(self, geom):
    """
    Set a new geometry to the analysis
    
    :param geom: The new geometry of the analysis
    :type geom: Geometry object
    """
    self.data["Geometry"] = geom   # pointer toward the geometry, so we can access the geometry defined in this class
    self.data["GeometryID"] = geom.data["ID"]
    return
  
  def setContext(self, context):
    """
    Set a new material distribution and boundary conditions to the analysis
    
    :param geom: The new material distribution and boundary condition of the analysis
    :type geom: Context object
    """
    self.context = context
    return
  
  def showProblem(self):
    """
    Plot the conceptual problem defined in the analysis (with material distribution)
    """
    fig,ax = self.data["Geometry"].draw(show=False)
    cmap = plt.get_cmap('tab20', np.max(list(self.data["Context"]["GeometryUsesMaterials"].values())))
    for reg, mat_id in self.data["Context"]["GeometryUsesMaterials"].items():
      pts = self["Geometry"]["Regions"][reg][0]
      X_pts = [self["Geometry"]["Points"][x-1,0] for x in pts]
      Y_pts = [self["Geometry"]["Points"][x-1,1] for x in pts]
      ax.fill(X_pts, Y_pts,color=cmap(mat_id-1))
    plt.show()
    return
