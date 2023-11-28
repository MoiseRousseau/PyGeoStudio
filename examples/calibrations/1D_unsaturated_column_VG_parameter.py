"""
Fit Van Genuchten parameters
============================
"""

import PyGeoStudio as pgs
import numpy as np

src_file = "../GeoStudio_files/1D_unsaturated_column.gsz"
copy_file = '.'.join(src_file.split('.')[:-1]) + "_tmp.gsz"
geofile_src = pgs.GeoStudioFile(src_file)
geofile_src.saveAs(copy_file)

# %%
# Open the copy and get the analysis of interest:
geofile = pgs.GeoStudioFile(copy_file)
mat = geofile.getMaterialByName("Material")
WCfunction = mat["Hydraulic"]["VolWCFn"]
Kfunction = mat["Hydraulic"]["KFn"]
instant_drawdown = geofile.getAnalysisByID(1)

# %%
# Create artificial experimental noisy data with actual Ksat as a target:
location = [0.05,0.8]
Tdata, PWPdata = instant_drawdown["Results"].getVariablesVsTime("PoreWaterPressure", locations=[location])
PWPdata += np.random.normal(0.,0.2,len(PWPdata)) #add some noise to measurement with std dev of 0.5 KPa

# %%
#
#set the X data 
N = 100 # number of data point
psi = np.logspace(-1,4,N) #suction from 0.1 to 1000 KPa
WCfunction.resizeXYData(N)
WCfunction.setXData(psi)
Kfunction.resizeXYData(N)
Kfunction.setXData(psi)
def run_model(xdata, new_log_Ksat, tets, a_log, n, tetr, m):
  new_Ksat = 10.**new_log_Ksat
  a = 10**a_log
  # set the new hydraulic conductivity function
  theta = pgs.builtin_functions.VanGenuchtenWC(psi,tets, a, n, tetr)
  WCfunction.setYData(theta)
  Krel = pgs.builtin_functions.VanGenuchtenMualemK(theta, m)
  Kfunction.setYData(new_Ksat * Krel)
  # run the analysis
  geofile.save()
  pgs.run(geofile, analyses_to_solve=[instant_drawdown])
  # return fitted data
  T,PWP = instant_drawdown["Results"].getVariablesVsTime("PoreWaterPressure", locations=[location])
  return PWP

# %%
# Calibrate and print results:
from scipy.optimize import curve_fit
initial_guess = [np.log10(4e-7), 0.3, np.log10(1), 2, 0.04, 2]
popt, pcov, info_dict, mesg, ier = curve_fit(
  run_model, Tdata, PWPdata, p0=initial_guess, full_output=True
)

from prettytable import PrettyTable
print("\n\n\nOptimisation results")
print("Optimisation information: ", info_dict)
print("Optimisation status: ", ier, " - ", mesg)
res = PrettyTable()
res.field_names = ["Parameter","Calibrated value","Target value"]
res.add_row(["Ksat", 10.**popt[0], 1e-6])
res.add_row(["Saturated Water Content", popt[1], 0.453])
res.add_row(["Air Entry Value", 10.**popt[2], 13])
res.add_row(["VG n", popt[3], 2.3])
res.add_row(["Resisual Water Content", popt[4], 1.5e-4])
res.add_row(["K relative m", popt[5], "User-defined"])
print(res)

# %%
# Get the modelled PWP in the last model runned:
T,PWP = instant_drawdown["Results"].getVariablesVsTime("PoreWaterPressure", locations=[location])

# %%
# Plot the calibrated model versus the experimental noisy data:
import matplotlib.pyplot as plt
fig,ax = plt.subplots()
ax.scatter(Tdata, PWPdata, color="k", label=f"Noisy experimental data")
ax.plot(Tdata, PWP, color="r", label=f"Calibrated model")
ax.grid()
ax.legend()
ax.set_ylabel("PoreWaterPressure")
ax.set_xlabel("Time (s)")
plt.tight_layout()
plt.show()
