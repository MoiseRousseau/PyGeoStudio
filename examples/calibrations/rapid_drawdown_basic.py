"""
Simple example fitting saturated hydraulic conductivity
=======================================================

"""


# %%
#This example illustrate how to use PyGeoStudio in an optimization process.
#The optimization carried here is the calibration of a hydrogeological model where the saturated conductivity of a material is being seek.
#We use the curve fitting function of SciPy library, which use the least square method (minimization of mean squared error) to fit experimental data.
#Experimental data are here generated synthetically buy adding articial noise to a reference solution.
#
#Note the curve fit function use information from the derivative of the model, which run a new simulation for each derivative relative to a calibrated parameter.
#This means if we calibrate 10 parameters with this method, 11 model simulations are carried per iteration (10 derivative + the current parameters being tested), and the number of iteration increase with the number of parameters.
# 
#Time to work!
#We use the `Rapid Drawdown <https://www.geoslope.com/learning/support-resources/example-files/example?id=examples:sigmaw:rapiddrawdown&resourceVersion=23.1.0.00000>`_ example problem from GeoStudio website.
#We first save a copy of the actual study (the calibration process modify the file in place):
import PyGeoStudio as pgs
import numpy as np

src_file = "../GeoStudio_files/Rapid drawdown.gsz"
copy_file = '.'.join(src_file.split('.')[:-1]) + "_tmp.gsz"
geofile_src = pgs.GeoStudioFile(src_file)
geofile_src.saveAs(copy_file)

# %%
# Open the copy and get the analysis of interest:
geofile = pgs.GeoStudioFile(copy_file)
mat = geofile.getMaterialByName("Dam fill")
Kfunction = mat["Hydraulic"]["KFn"]
instant_drawdown = geofile.getAnalysisByName("2 - Instantaneous drawdown")

# %%
# Create artificial experimental noisy data with actual Ksat as a target:
target_Ksat = Kfunction.getYData()[0]
Tdata, PWPdata = instant_drawdown["Results"].getVariablesVsTime("PoreWaterPressure", locations=[[25,2]])
PWPdata += np.random.normal(0.,1.5,len(PWPdata)) #add some noise to measurement with std dev of 1.5 KPa

# %%
# Below we define a function that receive new Ksat from the optimizer and return the fitted data value.
# The definition should follow what the ``scipy.optimize.curve_fit`` function expect (see `SciPy documentation <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html#scipy.optimize.curve_fit>`_), so we add the ``xdata`` dummy argument.
# Note most of the optimisation / calibration algorithm expects the parameters vary linearly, so we decided to calibrate the base 10 logarithm of the saturated hydraulic conductivity:
def run_model(xdata,new_log_Ksat):
  # set the new hydraulic conductivity function
  new_Ksat = 10.**new_log_Ksat
  actual_relK = Kfunction.getYData()
  actual_Ksat = Kfunction.getYData()[0]
  Kfunction.setYData(new_Ksat/actual_Ksat * actual_relK)
  # run the analysis
  geofile.save()
  pgs.run(geofile, analyses_to_solve=[instant_drawdown])
  # return fitted data
  T,PWP = instant_drawdown["Results"].getVariablesVsTime("PoreWaterPressure", locations=[[25,2]])
  return PWP

# %%
# Calibrate and print results:
from scipy.optimize import curve_fit
initial_guess_log = -7
popt, pcov, info_dict, mesg, ier = curve_fit(
  run_model, Tdata, PWPdata, p0=initial_guess_log, full_output=True
)
print("\n\n\nOptimisation results")
print("Optimal Ksat: ", 10.**popt[0], ", Target Ksat was:", target_Ksat)
print("Optimisation information: ", info_dict)
print("Optimisation status: ", ier, " - ", mesg)

# %%
# Get the modelled PWP in the last model runned:
T,PWP = instant_drawdown["Results"].getVariablesVsTime("PoreWaterPressure", locations=[[25,2]])

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
