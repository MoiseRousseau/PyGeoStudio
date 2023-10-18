import sys
import os
path = os.getcwd() + '/../../'
sys.path.append(path)

import PyGeoStudio as pgs

if __name__ == "__main__":
  src_file = "Reinforcement with Anchors.gsz" #specify the geostudio study file
  
  geofile = pgs.GeoStudioFile(src_file,mode='r') #open it with PyGeoStudio
  reinfs = geofile.getReinforcements() #get reinforcements defined in the study
  for reinf in reinfs: #print the reinforcement properties
    print(reinf)
    print("----------------------")
  
  # Change the pullout resistance of one anchor
  reinf1 = geofile.getReinforcementByName("New Reinforcement")
  reinf1["PulloutResistance"] = 350
  
  # Write back the study with the modified pullout resistance
  out_file = "./Reinforcement_with_Anchors_modified.gsz"
  geofile.writeGeoStudioFile(out_file)