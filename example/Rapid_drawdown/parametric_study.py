import sys
import os
path = os.getcwd() + '/../../'
sys.path.append(path)

import PyGeoStudio as pgs

if __name__ == "__main__":

  src_file = "temp.gsz" 
  geofile = pgs.GeoStudioFile(src_file)
  mat = geofile.getMaterialByName("Dam fill")
  
  Ksats = [1e-7, 1e-6, 1e-5, 1e-4]
  Ts = []
  PWPs = []
  
  for Ksat in Ksats:
    # change hydraulic conductivity
    mat["Hydraulic"]["KSat"] = Ksats
    # run GeoStudio
    geofile.save()
    pgs.run(geofile)
    # get results
    instant_drawdown = geofile.getAnalysisByName("2 - Instantaneous drawdown")
    T,PWP = instant_drawdown["Results"].getVariablesVsTime("PoreWaterPressure", locations=[[25,2]])
    # store it for future plotting
    Ts.append(T)
    PWPs.append(PWP)
  
  fig,ax = plt.subplots()
  ax.plot(
    Ts, PWPs,
    label=[str(x) for x in Ksats]
  )
  ax.grid()
  ax.legend()
  ax.set_ylabel("PoreWaterPressure")
  ax.set_xlabel("Time (s)")
  plt.tight_layout()
  plt.show()
