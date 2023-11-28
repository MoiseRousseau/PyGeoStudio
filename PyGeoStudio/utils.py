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

import subprocess
import PyGeoStudio
from .GeoPath import geopath

def defineGeoStudioLauncher(path):
  """
  Specify the path to GeoStudio installation to interac with the software (default set to ``C:\Program Files\Seequent\GeoStudio 2023.1``)
  
  :param path: Path to GeoStudio installation
  :type path: str
  """
  base_dir = "/".join(PyGeoStudio.__file__.split("/")[:-1])
  out = open(base_dir+"/GeoPath.py",'w')
  out.write(f"geopath = \"{path.rstrip()}\"")
  out.close()
  testLauncher(path.rstrip())
  return

def run(geofile, analyses_to_solve=None, shell=True):
  """
  Call GeoStudio solver to run the analyses defined in the GeoStudio file
  
  :param geofile: The GeoStudio file to run (path or opened study)
  :type geofile: GeoStudioFile object or str
  :param analyses_to_solve: A list of the analysis to run (optional, default all analyses)
  :type analyses_to_solve: list of PyGeoStudio.Analysis object
  :param shell: Show the console (optional, ``True`` by default)
  :type shell: bool
  """
  if isinstance(geofile, PyGeoStudio.GeoStudioFile):
    geofile = geofile.f_src
  if analyses_to_solve is not None:
    analyses_to_solve_name = [x["Name"] for x in analyses_to_solve]
  else:
    analyses_to_solve_name = []
  cmd = [geopath + "/Bin/GeoCmd.exe", geofile] + analyses_to_solve_name + ["/solve"]
  print("#################################")
  print("Calling GeoStudio solver")
  ret_code = subprocess.run(cmd, shell=shell)
  print(ret_code)
  print("#################################")
  return ret_code

def testLauncher(path=None):
  if path is None: path = geopath
  cmd = [path + "/Bin/GeoCmd.exe"]
  ret_code = subprocess.run(cmd, shell=True).returncode
  if ret_code != 0:
    raise ValueError("Can't find GeoStudio executables with the path provided. Please correct the path and redefine it with defineGeoStudioLauncher() method")
  else:
    print("Successfully tested GeoStudio executable")
  return
