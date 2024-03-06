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
import os, pathlib
import PyGeoStudio
from .GeoPath import geopath

def defineGeoStudioLauncher(path):
  """
  Specify the path to GeoStudio installation to interac with the software (default set to ``C:\Program Files\Seequent\GeoStudio 2023.1``)
  
  :param path: Path to GeoStudio installation
  :type path: str
  """
  base_dir = os.path.dirname(PyGeoStudio.__file__)
  out = open(os.path.join(base_dir, "GeoPath.py"),'w')
  s = str(pathlib.PureWindowsPath(path.rstrip()))
  out.write(f"geopath = \"{s}\"")
  out.close()
  testLauncher(s)
  return

def run(geofile, analyses_to_solve=None, shell=True, check_output=True):
  """
  Call GeoStudio solver to run the analyses defined in the GeoStudio file
  
  :param geofile: The GeoStudio file to run (path or opened study)
  :type geofile: GeoStudioFile object or str
  :param analyses_to_solve: A list of the analysis to run (optional, default all analyses)
  :type analyses_to_solve: list of PyGeoStudio.Analysis object
  :param shell: Show the console (optional, ``True`` by default)
  :type shell: bool
  :param check_output: Check if GeoStudio solver successfully solved the analysis
  :type check_output: bool
  """
  if isinstance(geofile, PyGeoStudio.GeoStudioFile):
    geofile = pathlib.PureWindowsPath(geofile.f_src)
  if analyses_to_solve is not None:
    analyses_to_solve_name = [x["Name"] for x in analyses_to_solve]
  else:
    analyses_to_solve_name = []
  cmd = [geopath + "\\Bin\\GeoCmd.exe", geofile] + analyses_to_solve_name + ["/solve"]
  print("#################################")
  print("Calling GeoStudio solver")
  cmd_out = subprocess.run(cmd, shell=shell)
  if check_output and cmd_out.returncode:
    message = "Call to GeoStudio ends up with no zero status code, which mean a failure of the simulation. Check GeoStudio output above for more detailed information."
    raise RuntimeError(message)
  print("#################################")
  return cmd_out.returncode

def testLauncher(path=None):
  if path is None: path = geopath
  cmd = [path + "\\Bin\\GeoCmd.exe", "/?"]
  error_message = "Can't find GeoStudio executables with the path provided. Please correct the path and redefine it with defineGeoStudioLauncher() method."
  try:
    output = subprocess.run(cmd, check=False, stdout=subprocess.PIPE).stdout.decode()
  except:
    raise ValueError(error_message)
  if "GeoCmd" in output and "Copyright" in output:
    print("GeoStudio version:" + output.split("\n")[0].split("version")[-1])
    print("Successfully tested GeoStudio executable")
  else:
    raise ValueError(error_message)
  return
