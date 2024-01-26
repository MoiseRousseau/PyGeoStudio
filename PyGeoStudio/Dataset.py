# This file is part of PyGeoStudio, an interface to GeoStudio 
# hydrogeotechnical software.
# Copyright (C) 2024, Moïse Rousseau
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

from .BasePropertiesClass import BasePropertiesClass
import numpy as np
import xml.etree.ElementTree as ET
import zipfile

class DatasetParameters:
  def __init__(self, prop):
    self.params = [param.text for param in prop]
    return

  def __write__(self, et):
    et.attrib = {"Len":str(len(self.params))}
    for p in self.params:
      sub = ET.SubElement(et, "Parameter")
      sub.text = p
    return

  def __str__(self):
    return ",".join(self.params)

  def __iter__(self):
    return self.params.__iter__()

  def __next__(self):
    return self.params.__next__()


class Dataset(BasePropertiesClass):
  """
  :param ID: Index of the dataset
  :type ID: int
  :param Name: Name of the dataset
  :type Name: str
  :param FilePath: Path to the dataset
  :type FilePath: str
  :param CsvID: ID of the dataset in GeoStudio file (do not change)
  :type CsvID: int
  :param NumRows: Number of record in the dataset (do not change)
  :type NumRows: int
  """

  parameter_type = {
    "ID" : int,
    "Name" : str,
    "FilePath" : str,
    "CsvID" : int,
    "Parameters" : DatasetParameters,
    "NumRows" : int,
  }

  my_data = ["Data"]

  dataset_parameters = {
    "AirTemperature" : "°C",
    "PotEvapotranspiration" : "",
    "PrecipitationRainfall" : "m",
    "Time" : "s",
    "WaterFlux" : "m3",
  }

  def __init__(self, prop, f_src):
    super().__init__(prop)
    src = zipfile.ZipFile(f_src)
    res = src.open(f"dataset_{self.data['CsvID']}.csv", 'r')
    self.data["Data"] = np.genfromtxt(res, delimiter=',', skip_header=1)[:,1:]
    res.close()
    src.close()
    return

  def loadDataFromCSV(self, path, delimiter=",", comments="#"):
    """
    Load data from a CSV file
    
    :param path: Path to the CSV file
    :type path: str
    """
    self.data["FilePath"] = path
    self.data["Data"] = np.genfromtxt(path,comments=comments, delimiter=delimiter)
    self.data["NumRows"] = self.data["Data"].shape[0]
    return

  def loadDataFromArray(self, arr):
    """
    Load data from the given array
    """
    self.data["Data"] = arr
    self.data["NumRows"] = arr.shape[0]
    return

  def setDataParameters(self, params):
    f"""
    Tells GeoStudio which kind of parameter this dataset represents
    
    :param params: List of the parameter name. Must match the available dataset parameter in GeoStudio: {self.dataset_parameters.keys()}
    :type params: list
    """
    if len(params) != self.data.shape[1]:
      raise ValueError("The list of parameter and number of column in the dataset should have the same length")
    for param in params:
      if param not in self.dataset_parameters.keys():
        raise ValueError(f"Parameter dataset {param} not recognized, must be one of {dataset_parameters.keys()}")
    self.data["Parameters"].params = params
    return
    
  def __str__(self):
    res = f"Dataset {self.data['Name']}\n"
    for i,x in enumerate(self.data["Parameters"]):
      res += f"Column {i}: {x} ({self.dataset_parameters[x]})\n"
    res += self.data["Data"].__str__()
    return res

