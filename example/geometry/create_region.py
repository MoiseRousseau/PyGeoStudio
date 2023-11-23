import sys
import os
path = os.getcwd() + '/../../'
sys.path.append(path)

import PyGeoStudio as pgs

if __name__ == "__main__":

  #open source geostudio study
  src_file = "test.gsz" 
  geofile = pgs.GeoStudioFile(src_file)
  
  #show geometry
  geofile.showGeometries()
  geometry = geofile.getGeometryByID(1)
  geometry.draw()
  
  #translate point 1
  points = geometry["Points"]
  points[0] += [-1,-1]
  #create new region
  new_region = [2,5,4]
  geometry.addRegions(new_region)
  #show new geometry
  geometry.draw()
  
  #write modified study under new file
  out_file = "./test2.gsz"
  geofile.saveAs(out_file)
  
