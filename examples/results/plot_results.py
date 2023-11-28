"""
Extract and plot results from analysis
======================================

"""

# %%
# This examples illustrates how to extract results from SEEP/W analyses and plot it using ``matplotlib``.
# First open the study Rapid Drawdown <https://www.geoslope.com/learning/support-resources/example-files/example?id=examples:sigmaw:rapiddrawdown&resourceVersion=23.1.0.00000>`_ from GeoStudio website:
import PyGeoStudio as pgs
src_file = "../GeoStudio_files/Rapid drawdown.gsz"
geofile = pgs.GeoStudioFile(src_file)
instant_drawdown = geofile.getAnalysisByName("2 - Instantaneous drawdown")

# %%
# Get the results from the instantaneous drawdown analysis and print variable solved and timestep saved:
results = instant_drawdown["Results"]
print(results.getOutputVariables())
print(results.getOutputTimes())

# %%
# Plot the Pore Water Pressure variable at point x=25 and y=2 versus time:
import matplotlib.pyplot as plt
T,PWP = results.getVariablesVsTime("PoreWaterPressure", locations=[[25,2],[23,1]])
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
