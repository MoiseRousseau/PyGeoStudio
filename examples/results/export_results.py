"""
Export results to Paraview
==========================

"""

# %%
# This simple example shows how to extract meshes and results from GeoStudio analyses to post-process them with Paraview
# The `Rapid Drawdown <https://www.geoslope.com/learning/support-resources/example-files/example?id=examples:sigmaw:rapiddrawdown&resourceVersion=23.1.0.00000>`_ example problem GeoStudio website is used.
# We first open the study and get the analysis of interest:
import PyGeoStudio as pgs
src_file = "../GeoStudio_files/Rapid drawdown.gsz" #specify the geostudio analyses file
geofile = pgs.GeoStudioFile(src_file) #open it with PyGeoStudio
instant_drawdown = geofile.getAnalysisByName("2 - Instantaneous drawdown") #select analysis 2 with instant drawdown

# %%
# Exporting results to Paraview in VTU format is carried by a one line command.
# This will create several ``res.vtu.XXX`` files, each for one timestep saved in the analysis.
instant_drawdown["Results"].exportAllResultsVTU("res.vtu")

# %%
# If only the mesh is needed, for example, to perform mesh analysis, the following command can be used:
instant_drawdown["Geometry"]["Mesh"].export("mesh.vtk")
