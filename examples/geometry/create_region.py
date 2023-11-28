"""
Geometry basics
===============

"""

# %%
# Open example GeoStudio study
import PyGeoStudio as pgs
src_file = "../GeoStudio_files/test.gsz"
geofile = pgs.GeoStudioFile(src_file)

# %%
# Show the geometries defined in the study and select the one with ID 1 to draw it
geofile.showGeometries()
geometry = geofile.getGeometryByID(1)
geometry.draw()

# %%
# Get the points defined in the geometry and translate the first one by (-1,-1):
points = geometry["Points"]
points[0] += [-1,-1]

# %%
# Create a new region from point IDs:
new_region = [2,5,4]
geometry.addRegions(new_region)
geometry.draw()

# %%
# Write modified study under new file:
out_file = "./test2.gsz"
geofile.saveAs(out_file)
  
