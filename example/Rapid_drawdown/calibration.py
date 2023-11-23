import sys
import os
import shutil
path = os.getcwd() + '/../../'
sys.path.append(path)

import PyGeoStudio as pgs
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


# Save a copy of the actual study (the calibration process modify the file in place)
src_file = "Rapid drawdown.gsz"
copy_file = '.'.join(src_file.split('.')[:-1]) + "_tmp.gsz"
geofile_src = pgs.GeoStudioFile(src_file)
geofile_src.saveAs(copy_file)

# Open the copy and get object of interest
geofile = pgs.GeoStudioFile(copy_file)
mat = geofile.getMaterialByName("Dam fill")
Kfunction = mat["Hydraulic"]["KFn"]
instant_drawdown = geofile.getAnalysisByName("2 - Instantaneous drawdown")

# Create artificial experimental data with actual Ksat as a target
target_Ksat = Kfunction.getYData()[0]
Tdata, PWPdata = instant_drawdown["Results"].getVariablesVsTime("PoreWaterPressure", locations=[[25,2]])
PWPdata += np.random.normal(0.,1.5,len(PWPdata)) #add some noise to measurement with std dev of 3 KPa

# define a function that receive new Ksat from the optimizer and return the fitted data value
#Note the xdata 
def run_model(xdata,new_log_Ksat):
  # set the new hydraulic conductivity function
  new_Ksat = 10.**new_log_Ksat
  actual_relK = Kfunction.getYData()
  actual_Ksat = Kfunction.getYData()[0]
  Kfunction.setYData(new_Ksat/actual_Ksat * actual_relK)
  # run the analysis
  geofile.save()
  pgs.run(geofile, analyses_to_solve=["2 - Instantaneous drawdown"])
  # return fitted data
  T,PWP = instant_drawdown["Results"].getVariablesVsTime("PoreWaterPressure", locations=[[25,2]])
  return PWP
  
# Optimize
initial_guess = -7
popt, pcov, info_dict, mesg, ier = curve_fit(
  run_model, Tdata, PWPdata, p0=initial_guess, full_output=True
)

# Print results
print("\n\n\nOptimisation results")
print("Optimal Ksat: ", 10.**popt[0], ", Target Ksat was:", target_Ksat)
print("Optimisation information: ", info_dict)
print("Optimisation status: ", ier, " - ", mesg)

# Plot the calibrated model versus the experimental noisy data
# get the optimized PWP in the last model runned
T,PWP = instant_drawdown["Results"].getVariablesVsTime("PoreWaterPressure", locations=[[25,2]])
# plot it
fig,ax = plt.subplots()
ax.scatter(Tdata, PWPdata, color="k", label=f"Noisy experimental data")
ax.plot(Tdata, PWP, color="r", label=f"Calibrated model")
ax.grid()
ax.legend()
ax.set_ylabel("PoreWaterPressure")
ax.set_xlabel("Time (s)")
plt.tight_layout()
plt.show()
