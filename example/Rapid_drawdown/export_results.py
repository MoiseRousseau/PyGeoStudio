import sys
import os
path = os.getcwd() + '/../../'
sys.path.append(path)

import PyGeoStudio as pgs
import matplotlib.pyplot as plt

if __name__ == "__main__":
  src_file = "Rapid drawdown.gsz" #specify the geostudio analyses file
  
  geofile = pgs.GeoStudioFile(src_file,mode='r') #open it with PyGeoStudio
  geofile.showAnalysisTree() #print analyses in the file

  instant_drawdown = geofile.getAnalysisByName("2 - Instantaneous drawdown") #select analysis 2 with instant drawdown
  
  # export only the mesh in VTK format
  mesh = instant_drawdown["Geometry"]["Mesh"]
  mesh.export("mesh.vtk")
  
  # export all results to VTU format for post-processing with Paraview
  instant_drawdown["Results"].exportAllResultsVTU("res.vtu")
