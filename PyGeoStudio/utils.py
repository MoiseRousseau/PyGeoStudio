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
import os, pathlib, sys
import PyGeoStudio


def getGeoStudioVersion():
  """
  Test if PyGeoStudio is able to launch GeoStudio. GeoStudio executables should be on the system path.
  By default, the path ``C:\Program Files\Seequent\GeoStudio 20XX,Y`` are appended, so it directly finds the lastest GeoStudio version if not found in system path.
  """mmon_path = [
    "C:/Program Files/Seequent/GeoStudio 2024.2/Bin/",
    "C:/Program Files/Seequent/GeoStudio 2024.1/Bin/",
    "C:/Program Files/Seequent/GeoStudio 2023.1/Bin/",
    "C:/Program Files/Seequent/GeoStudio 2022.1/Bin/",
    "C:/Program Files/Seequent/GeoStudio 2021.4/Bin/",
    "C:/Program Files/Seequent/GeoStudio 2021.3/Bin/",
    "C:/Program Files/Seequent/GeoStudio 2021 R2/Bin/",
    "C:/Program Files/Seequent/GeoStudio 2021/Bin/",
  ]
  common_path = [str(pathlib.PureWindowsPath(x)) for x in common_path]
  os.environ["PATH"] += os.pathsep + os.pathsep.join(common_path)
  cmd = ["GeoCmd.exe", "/?"]
  error_message = "Error running GeoStudio. Please correct the path, restart Python and retry."
  try:
    output = None
    output = subprocess.run(cmd, check=False, stdout=subprocess.PIPE).stdout.decode()
    version = output.split("\n")[0].split("version")[-1].strip()
  except:
    print(output)
    raise ValueError(error_message)
  return version

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
  cmd = ["GeoCmd.exe", geofile] + analyses_to_solve_name + ["/solve"]
  print("#################################")
  print("Calling GeoStudio solver")
  cmd_out = subprocess.run(cmd, shell=shell)
  if check_output and cmd_out.returncode:
    message = "Call to GeoStudio ends up with no zero status code, which mean a failure of the simulation. Check GeoStudio output above for more detailed information."
    raise RuntimeError(message)
  print("#################################")
  return cmd_out.returncode
