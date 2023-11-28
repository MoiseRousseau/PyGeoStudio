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

import xml.etree.ElementTree as ET
from .BasePropertiesClass import BasePropertiesClass
import matplotlib.pyplot as plt
import numpy as np

class Function(BasePropertiesClass):
  """
  :param ID: ID of the function (must not be changed)
  :type ID: int
  :param Name: Name of the function
  :type Name: str
  :param Points: XY points to be interpolated and that defined the function
  :type Points: numpy array
  :param Function:
  :type Function:
  :param Estimate:
  :type Estimate:
  :param Types: Type of function. For example, for a function defining a water retention curve of a material, function type is ``["Material", "Hydraulic", "VolWCFun"]``.
  :type Types: list of str
  """
  parameter_type = {
    "ID" : int,
    "Name" : str,
    "Points" : list,
    "Function" : str,
    "Estimate" : str,
    "Types" : list,
    "FunctionParameter" : dict,
    "FunctionType" : str,
  }
  my_data = ["Types", "FunctionParameter", "FunctionType"]

  def __getitem__(self, property_):
    if property_ == "FunctionParameter":
      return self.fun_options
    elif property_ == "FunctionType":
      return self.fun_type
    else:
      return super().__getitem__(property_)

  def plot(self):
    """
    Plot the function data using matplotlib
    """
    fig,ax = plt.subplots()
    X = self.data["Points"][:,0]
    Y = self.data["Points"][:,1]
    ax.plot(X,Y,'r', label=self.data["Name"])
    ax.set_xlabel(self.fun_options["InputParam"])
    ax.set_ylabel(self.fun_options["OutputParam"])
    if self.fun_options["LogInput"]: ax.set_yscale('log')
    if self.fun_options["LogOutput"]: ax.set_yscale('log')
    ax.grid()
    ax.legend()
    plt.show()
    return
  
  def getXData(self):
    """
    Helper method to extract the X data of the Points attribute.

    :return: The X datapoints of the function
    :rtype: numpy array
    """
    return self.data["Points"][:,0]

  def setXData(self, values):
    """
    Helper method to set the X data of the Points attribute.
    Size must match the actual X data.

    :param values: The new X data
    :type values: numpy array or list
    """
    self.data["Points"][:,0] = values
    return

  def getYData(self):
    """
    Helper to extract the Y data of the Points attribute.

    :return: The Y datapoints of the function
    :rtype: numpy array
    """
    return self.data["Points"][:,1]

  def setYData(self, values):
    """
    Helper method to set the Y data of the Points attribute.
    Size must match the actual Y data.

    :param values: The new Y data
    :type values: numpy array or list
    """
    self.data["Points"][:,1] = values
    return

  def resizeXYData(self, n):
    """
    Resize the function XY data and fill it with zeros.
    
    :param n: New size of the X and Y data array
    :type n: int
    """
    self.data["Points"] = np.zeros((n,2), dtype="f8")
    return

  def __initialize__(self):
    if self.data.get("Points") is not None:
      self.data["Points"] = np.array( [ [float(y) for y in x[1].values()] for x in self.data["Points"] ] )
    options = [ x.split('=') for x in self.data["Function"].split('(')[-1][:-1].split(',') ]
    self.fun_options = {x[0] : x[1] for x in options }
    self.fun_type = self.data["Function"].split('(')[0]
    return
  
  def __deinitialize__(self):
    if self.data.get("Points") is not None:
      self.data["Points"] = [
        ["Point", {"X":str(x), "Y":str(y)}] for x,y in self.data["Points"]
      ]
    return
