import sys
import os
path = os.getcwd() + '/../../'
sys.path.append(path)

import PyGeoStudio as pgs

if __name__ == "__main__":
  src_file = "Rapid drawdown.gsz" #specify the geostudio analyses file
  
  geofile = pgs.GeoStudioFile(src_file,mode='r') #open it with PyGeoStudio
  geofile.showAnalysisTree() #print analyses in the file
  
  instant_drawdown = geofile["2 - Instantaneous drawdown"] #select step 2 with instant drawdown
  instant_drawdown.showProblem() #draw the conceptual model using matplotlib
  
  #print variable solved in instant_drawdown problem and timestep saved
  print(instant_drawdown.getOutputVariables())
  print(instant_drawdown.getOutputTimes())
  
  #plot the pore water pressure at point x=25,y=2 versus time using matplotlib
  instant_drawdown.plotResults("PoreWaterPressure", location=[25,2])
