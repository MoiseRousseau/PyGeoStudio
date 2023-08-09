import sys
import os
path = os.getcwd() + '/../../'
sys.path.append(path)

import PyGeoStudio as pgs

if __name__ == "__main__":

  #open source geostudio study
  src_file = "test.gsz" 
  geofile = pgs.GeoStudioFile(src_file,mode='r')
  
  #show geometry
  geofile.printGeometries()
  geometry = geofile.getGeometry(1)
  geometry.showGeometry()
  
  #translate point 1
  points = geometry.getPoints()
  points[0] += [-1,-1]
  #create new region
  new_region = [2,5,4]
  geometry.addRegion(new_region)
  #show new geometry
  geometry.showGeometry()
  
  #write modified study under new file
  out_file = "./test2.gsz"
  geofile.writeGeoStudioFile(out_file)
  geofile2 = pgs.GeoStudioFile(out_file,mode='r')
  
