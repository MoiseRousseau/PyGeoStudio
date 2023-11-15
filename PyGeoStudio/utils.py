import subprocess
from .PyGeoStudio import GeoStudioFile
from .GeoPath import geopath

def defineGeoStudioLauncher(path):
  """
  Specify the path to GeoStudio installation to interac with the software (default set to ``C:\Program Files\Seequent\GeoStudio 2023.1``)
  
  :param path: Path to GeoStudio installation
  :type path: str
  """
  out = open("GeoPath.py",'w')
  out.write(f"geopath = \"{path.rstrip()}\"")
  out.close()
  return

def run(geofile, analyses_to_solve=None, shell=True):
  """
  Call GeoStudio solver to run the analyses defined in the GeoStudio file
  
  :param geofile: The GeoStudio file to run
  :type geofile: GeoStudioFile object or str
  :param analyses_to_solve: A list of the analysis to run (optional, default all analyses)
  :type analyses_to_solve: list of str
  :param shell: Show the console 
  :type shell: bool
  """
  cmd = [geopath + "/Bin/GeoCmd.exe", geofile] + analyses_to_solve + ["/solve"]
  print("#################################")
  print("Calling GeoStudio solver")
  ret_code = subprocess.run(cmd, shell=shell)
  print(ret_code)
  print("#################################")
  return ret_code
