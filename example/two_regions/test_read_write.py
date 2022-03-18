import sys
import os
path = os.getcwd() + '/../../'
sys.path.append(path)

import PyGeoStudio as pgs

if __name__ == "__main__":
  src_file = "test.gsz" #specify the geostudio analyses file
  out_file = "./test2.gsz"
  
  geofile = pgs.GeoStudioFile(src_file,mode='r') #open it with PyGeoStudio
  geofile.writeGeoStudioFile(out_file)
  geofile2 = pgs.GeoStudioFile(out_file,mode='r')
  
  print(geofile2 == geofile)
  
