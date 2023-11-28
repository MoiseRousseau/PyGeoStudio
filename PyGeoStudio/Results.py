# This file is part of PyGeoStudio, an interface to GeoStudio 
# hydrogeotechnical software.
# Copyright (C) 2023, Moïse Rousseau
# 
# PyGeoStudio is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PyGeoStudio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numpy as np
import zipfile

from .BasePropertiesClass import BasePropertiesClass

class Results:
  def __init__(self, f_src, analysis, mesh=None):
    self.f_src = f_src
    self.analysis = analysis
    self.analysis_name = analysis["Name"]
    self.saved_time = None
    if self.analysis["Method"] == "Transient":
      self.saved_time = tuple((i+1,float(x["ElapsedTime"])) for i,x in enumerate(analysis["TimeIncrements"]["TimeSteps"]) if x.get("Save"))
    self.mesh = mesh
    return

  def getOutputVariables(self):
    """
    Return a list of the output variables in the results
    
    :return: the list
    :rtype: list
    """
    src = zipfile.ZipFile(self.f_src)
    res = src.open(f"{self.analysis_name.replace('/','&3')}/{0:0>3d}/node.csv", 'r')
    header = res.readline().decode().rstrip().split(',')
    res.close()
    src.close()
    return header
  
  def getOutputTimes(self):
    """
    Return the timestep saved
    
    :return: The timestep
    :rtype: list
    """
    return [x[1] for x in self.saved_time] #return a copy
  
  def getSnapshot(self, variable, time=None):
    """
    Extract the variable on the whole domain but at one particular time.
    
    :param variable: Name of variable desired (must match the name from ``getOutputVariables``)
    :type variable: str
    :param time: Time at which to retrieve variable value (required for transient analysis)
    :type time: float
    :return: Variable values ordered by node ID
    :rtype: numpy.array
    """
    if self.analysis["Method"] == "Transient" and time is None:
      raise ValueError("Transient analysis results requires the time to extract the snapshot")
    try:
      variable_index = self.getOutputVariables().index(variable)
    except:
      raise ValueError(f"Output variables \"{variable}\" not found in file. Available output variables are: {self.getOutputVariables()}")
    src = zipfile.ZipFile(self.f_src)
    t_index = [x[1] for x in self.saved_time].index(time)
    f = src.open(f"{self.analysis_name.replace('/','&3')}/{t_index:0>3d}/node.csv")
    data = np.genfromtxt(f, delimiter=',', skip_header=1)[:,variable_index] #remove point id
    f.close()
    src.close()
    return data
    
  def getVariablesVsTime(self, variable, locations):
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
    src = zipfile.ZipFile(self.f_src)
    champions = [0 for i in range(len(locations))]
    for i,location in enumerate(locations):
      champions[i] = self.mesh.getPointIndexInMesh(location)
    datas = [None for i in self.saved_time]
    temp = np.zeros(len(locations), dtype='f8')
    for j,timestep in enumerate(self.saved_time):
      i = timestep[0]
      temp[:] = np.nan
      f = src.open(f"{self.analysis_name.replace('/','&3')}/{i:0>3d}/node.csv")
      data = np.genfromtxt(f, delimiter=',', skip_header=1)
      index_in_results = [int(np.argwhere(data[:,0] == x)) for x in champions]
      datas[j] = data[index_in_results,variable_index]
      f.close()
    final_datas = np.array(datas)
    src.close()
    X = np.zeros_like(final_datas) + np.array([x[1] for x in self.saved_time])[:,None]
    Y = final_datas
    if len(locations) == 1:
      X = X.squeeze()
      Y = Y.squeeze()
    return X,Y
  
  def exportAllResultsVTU(self, path):
    """
    Export all the results of the analysis for post-processing with Paraview software. Export is handle by MeshIO.
    
    :param path: Path to the output file
    :type path: str
    """
    try:
      import meshio
    except:
      raise RuntimeError("Please install MeshIO to use this capability")
    
    points, cells = self.mesh.asMeshIOData()
    for i,timestep in enumerate(self.saved_time):
      t = timestep[1]
      point_data = {variable:self.getSnapshot(variable, t) for variable in self.getOutputVariables()}
      out_mesh = meshio.Mesh(points=points, cells=cells, point_data=point_data)
      out_mesh.write(path+f".{i:0>3d}", file_format="vtu")
    return
    
  def exportAllResultsXDMF(self, path):
    """
    Export all the results (all timestep) of the analysis for post-processing. Export is handle by MeshIO.
    
    :param path: Path to the output file
    :type path: str
    :meta private:
    """
    try:
      import meshio, h5py
    except:
      raise RuntimeError("Please install MeshIO and h5py to use this capability")
    
    points, cells = self.mesh.asMeshIOData()
    with meshio.xdmf.TimeSeriesWriter(path) as writer:
      writer.write_points_cells(points, cells)
      for timestep in self.saved_time:
        t = timestep[0]
        point_data = {variable:self.getSnapshot(variable, t) for variable in self.getOutputVariables()}
        print(point_data["Node"][20], point_data["PoreWaterPressure"][20])
        writer.write_data(t, point_data=point_data)
    return
