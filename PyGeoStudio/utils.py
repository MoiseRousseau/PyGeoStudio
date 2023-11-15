import subprocess
from .PyGeoStudio import GeoStudioFile

def defineGeoStudioLauncher(path):
  """
  Specify the path to GeoStudio installation to interac with the software (default set to ``C:\Program Files\Seequent\GeoStudio 2023.1``)
  
  :param path: Path to GeoStudio installation
  :type path: str
  """
  this_path = "/".join(__file__.split("/")[:-1])
  out = open(this_path + "/GeoStudio_path.txt",'w')
  out.write(path)
  out.close()
  return

def run(geofile, analysis_name=None, shell=True):
  """
  Call GeoStudio solver to run the analyses defined in the GeoStudio file
  
  :param geofile: The GeoStudio file to run
  :type geofile: GeoStudioFile object or str
  :param analysis_name: A list of the analysis to run (optional, default all analyses)
  :type analysis_name: list
  :param shell: Show the console 
  :type shell: bool
  """
  if isinstance(geofile, GeoStudioFile):
    geofile = geofile.f_src
  this_path = "/".join(__file__.split("/")[:-1])
  with open(this_path + '/GeoStudio_path.txt', 'r') as f:
    base_path = f.readline().rstrip()
  cmd = [base_path+"/Bin/GeoCmd.exe", geofile, "/solve"]
  print("#################################")
  print("Calling GeoStudio solver")
  ret_code = subprocess.run(cmd, shell=shell)
  print(ret_code)
  print("#################################")
  return ret_code
