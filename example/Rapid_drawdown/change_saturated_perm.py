import sys
import os
path = os.getcwd() + '/../../'
sys.path.append(path)

import PyGeoStudio as pgs

if __name__ == "__main__":
  src_file = "Rapid drawdown.gsz" #specify the geostudio analyses file
  
  geofile = pgs.GeoStudioFile(src_file,mode='r') #open it with PyGeoStudio
  mats = geofile.getMaterials() #get material defined in the analysis
  for mat in mats: #print the material name properties
    print(mat)
    print("----------------------")
  
  mat = geofile.getMaterialByName("Toe drain") #get material nammed "Toe drain"
  mat["Hydraulic"]["KSat"] = 1e-6 #change its saturated permeability
  print(mat)
  
  #write modified study under new file
  print("----------------------")
  print("Write modified study in rapid_drawdown_changed_perm.gsz")
  out_file = "./rapid_drawdown_changed_perm.gsz"
  geofile.writeGeoStudioFile(out_file)
