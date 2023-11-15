import sys
import os
path = os.getcwd() + '/../../'
sys.path.append(path)

import PyGeoStudio as pgs
import matplotlib.pyplot as plt

if __name__ == "__main__":

  src_file = "Rapid drawdown.gsz" 
  geofile = pgs.GeoStudioFile(src_file)
  mat = geofile.getMaterialByName("Dam fill")
  
  Ksats = [1e-7, 1e-6, 1e-5, 1e-4]
  Ts = []
  PWPs = []
  
  for Ksat in Ksats:
    # change hydraulic conductivity
    mat["Hydraulic"]["KSat"] = Ksat
    # run GeoStudio
    geofile.save()
    pgs.run(geofile, analyses_to_solve=["2 - Instantaneous drawdown"])
    # get results
    instant_drawdown = geofile.getAnalysisByName("2 - Instantaneous drawdown")
    T,PWP = instant_drawdown["Results"].getVariablesVsTime("PoreWaterPressure", locations=[[25,2]])
    # store it for future plotting
    Ts.append(T)
    PWPs.append(PWP)
  
  fig,ax = plt.subplots()
  for T,PWP,Ksat in zip(Ts,PWPs,Ksats):
    ax.plot(T, PWP, label=f"Ksat = {Ksat}")
  ax.grid()
  ax.legend()
  ax.set_ylabel("PoreWaterPressure")
  ax.set_xlabel("Time (s)")
  plt.tight_layout()
  plt.show()
