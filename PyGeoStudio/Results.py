import numpy as np

from .BasePropertiesClass import BasePropertiesClass

class Results:
  def __init__(self, geofile, analysis_name, time, mesh=None):
    self.geofile = geofile
    self.analysis_name = analysis_name
    self.time = time
    self.mesh = mesh
    return

  def getOutputVariables(self):
    """
    Return a list of the output variables in the results
    
    :return: the list
    :rtype: list
    """
    res = self.geofile.open(f"{self.analysis_name.replace('/','&3')}/{1:0>3d}/node.csv", 'r')
    header = res.readline().decode().rstrip().split(',')
    res.close()
    return header
  
  def getOutputTimes(self):
    """
    Return the timestep saved
    
    :return: The timestep
    :rtype: list
    """
    return list(self.time) #return a copy
    
  def getVariablesVsTime(self, variable, locations):
    #TODO: does not work
    """
    Extract the variable at the locations given against all timestep.
    
    :param variable: Name of variable desired (must match the name from ``getOutputVariables``)
    :type variable: str
    :param locations: Location at which to retrive variable value
    :type locations: list
    :return: Time and variable values at different location and all times
    :rtype: numpy.array, numpy.array
    """
    #check if variable is output and get its index
    try:
      variable_index = self.getOutputVariables().index(variable)
    except:
      raise ValueError(f"Output variables \"{variable}\" not found in file. Available output variables are: {self.getOutputVariables()}")
    champions = [0 for i in range(len(locations))]
    for i,location in enumerate(locations):
      champions[i] = self.mesh.getPointIndexInMesh(location)
    datas = [None for i in self.time]
    temp = np.zeros(len(locations), dtype='f8')
    for i in range(len(self.time)):
      temp[:] = np.nan
      f = self.geofile.open(f"{self.analysis_name.replace('/','&3')}/{i:0>3d}/node.csv")
      data = np.genfromtxt(f, delimiter=',', skip_header=1)
      index_in_results = [int(np.argwhere(data[:,0] == x)) for x in champions]
      datas[i] = data[index_in_results,variable_index]
      f.close()
    final_datas = np.array(datas)
    return np.zeros_like(final_datas) + np.array(self.time)[:,None], final_datas
  
  def exportResults(self, fmt='VTK', variables=None, ):
    """
    Export the results of the analysis for post-processing with another software (e.g. Paraview)
    
    :meta private:
    """
    #TODO
    return
