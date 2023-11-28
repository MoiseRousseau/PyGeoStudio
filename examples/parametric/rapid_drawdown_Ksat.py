"""
Effect of saturated permeability on drawdown problem
====================================================
"""

# %%
# This example constitutes a simple demonstration of how to conduct a parametric study.
# The `Rapid Drawdown <https://www.geoslope.com/learning/support-resources/example-files/example?id=examples:sigmaw:rapiddrawdown&resourceVersion=23.1.0.00000>`_ example problem GeoStudio website is used.
# The parametric study consists of analyzing the effect of the saturated hydraulic conductivity of the dam on the dissipation of the pore water pressure following a instantaneous drawdown.
# 
# We first import ``PyGeoStudio`` library, open the GeoStudio study and get hydraulic permeability function of the dam fill material.

import PyGeoStudio as pgs

src_file = "../GeoStudio_files/Rapid drawdown.gsz"
geofile = pgs.GeoStudioFile(src_file)
mat = geofile.getMaterialByName("Dam fill")
Kfunction = mat["Hydraulic"]["KFn"]


# %%
# Then we define the saturated hydraulic conductivity to test in our parametric study and initiate Python list to get the results of the simulation.

Ksats = [1e-7, 1e-6, 1e-5, 1e-4]
Ts = []
PWPs = []

# %%
# We now enter in the parametric study loop to analyze the pore water pressure dissipation for the different ``Ksat``.
# Note there is no way in GeoStudio to define the saturated hydraulic conductivity of the unsaturated material.
# The saturated hydraulic conductivity is rather specified through the hydraulic function.
# So the approach is to scale the whole conductivity function.

for new_Ksat in Ksats:
  # scale hydraulic conductivity
  # note relative permeability is defined through the function,
  # not by the KSat attribute which is for saturated only model
  actual_relK = Kfunction.getYData()
  actual_Ksat = Kfunction.getYData()[0]
  Kfunction.setYData(new_Ksat/actual_Ksat * actual_relK)
  # run GeoStudio
  geofile.save()
  instant_drawdown = geofile.getAnalysisByName("2 - Instantaneous drawdown")
  pgs.run(geofile, analyses_to_solve=[instant_drawdown])
  # get results
  T,PWP = instant_drawdown["Results"].getVariablesVsTime(
    "PoreWaterPressure",
    locations=[[25,2]]
  )
  # store it for future plotting
  Ts.append(T)
  PWPs.append(PWP)


# %%
# The ``PWPs`` list now contains the pore water pressure dissipation curves for the different conductivity tested.
# We can plot these curves using ``matplotlib`` library:
import matplotlib.pyplot as plt
fig,ax = plt.subplots()
for T,PWP,Ksat in zip(Ts,PWPs,Ksats):
  ax.plot(T, PWP, label=f"Ksat = {Ksat}")
ax.grid()
ax.legend()
ax.set_ylabel("PoreWaterPressure")
ax.set_xlabel("Time (s)")
plt.tight_layout()
plt.show()
