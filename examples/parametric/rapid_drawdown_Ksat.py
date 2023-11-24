"""
Effect of saturated permeability on drawdown problem
====================================================

"""

import sys
import os
path = os.getcwd() + '/../../'
sys.path.append(path)

import PyGeoStudio as pgs
import matplotlib.pyplot as plt

if __name__ == "__main__":

  src_file = "../GeoStudio_files/Rapid drawdown.gsz"
  geofile = pgs.GeoStudioFile(src_file)
  mat = geofile.getMaterialByName("Dam fill")

  # get function defining material unsaturated hydraulic conductivity
  Kfunction = mat["Hydraulic"]["KFn"]

  # parameter to test and structure for results
  Ksats = [1e-7, 1e-6, 1e-5, 1e-4]
  Ts = []
  PWPs = []

  for new_Ksat in Ksats:
    # scale hydraulic conductivity
    # note relative permeability is defined through the function, not by the KSat attribute which is for saturated only model
    actual_relK = Kfunction.getYData()
    actual_Ksat = Kfunction.getYData()[0]
    Kfunction.setYData(new_Ksat/actual_Ksat * actual_relK)
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
