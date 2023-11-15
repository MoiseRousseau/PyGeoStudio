import sys
import os
path = os.getcwd() + '/../../'
sys.path.append(path)

import PyGeoStudio as pgs
import matplotlib.pyplot as plt

if __name__ == "__main__":
  src_file = "Rapid drawdown.gsz" #specify the geostudio analyses file
  
  geofile = pgs.GeoStudioFile(src_file) #open it with PyGeoStudio
  geofile.showAnalysisTree() #print analyses in the file
  print(geofile["Analyses"]) #return low level pygeostudio.analysis objects representing the analyses

  instant_drawdown = geofile.getAnalysisByName("2 - Instantaneous drawdown") #select analysis 2 with instant drawdown
  #instant_drawdown.showProblem() #draw the conceptual model using matplotlib
  
  #print variable solved in instant_drawdown problem and timestep saved
  print(instant_drawdown["Results"].getOutputVariables())
  print(instant_drawdown["Results"].getOutputTimes())
  
  #plot the pore water pressure at point x=25,y=2 versus time using matplotlib
  T,PWP = instant_drawdown["Results"].getVariablesVsTime("PoreWaterPressure", locations=[[25,2],[23,1]])
  fig,ax = plt.subplots()
  ax.plot(
    T, PWP,
    label=["x=25,y=2","x=23,y=1"]
  )
  ax.grid()
  ax.legend()
  ax.set_ylabel("PoreWaterPressure")
  ax.set_xlabel("Time (s)")
  plt.tight_layout()
  plt.show()
