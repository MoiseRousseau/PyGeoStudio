"""
Change timestep options
=======================

"""

# %%
# This example shows how to interact with analysis timesteps.
# We first import PyGeoStudio and open the study
import numpy as np
import PyGeoStudio as pgs
src_file = "../GeoStudio_files/Rapid drawdown.gsz" #specify the geostudio analyses file
geofile = pgs.GeoStudioFile(src_file) #open it with PyGeoStudio

# %%
# Timesteps are defined in analysis, and can retrieven with
geofile.showAnalysisTree()
analysis = geofile.getAnalysisByID(4)
timestepping = analysis["TimeIncrements"]

# %%
# Print timestep details:
timestepping.showTimeSteps()

# %%
# Set new timesteps:
end = timestepping["Duration"]
new_times = list(np.logspace(2,np.log10(end),50)) #exponential timesteps
saved = [False for x in new_times]
new_times += [1000, 1e4, 1e6, 1e6] #add user defined timesteps
saved += [True] * 4
timestepping.setTimeSteps(new_times, saved)

# %%
# Modification can be saved under a new file
print("----------------------")
out_file = "./rapid_drawdown_changed_timestep.gsz"
geofile.saveAs(out_file)
