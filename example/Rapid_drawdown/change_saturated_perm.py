import sys
import os
path = os.getcwd() + '/../../'
sys.path.append(path)

import PyGeoStudio as pgs

if __name__ == "__main__":
  src_file = "Rapid drawdown.gsz" #specify the geostudio analyses file
  
  geofile = pgs.GeoStudioFile(src_file,mode='r') #open it with PyGeoStudio
  mats = geofile.getMaterials()
  for mat in mats:
    print(mat)
    print("----------------------")
  
  mat = geofile.getMaterialByName("Toe drain")
  mat.hydraulic_function["KSat"] = str(1e-6)
  print(mat)
  
