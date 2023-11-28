"""
Change material properties
==========================

"""

# %%
# This example shows how to list, select and interact with material
# We first import PyGeoStudio and open the study

import PyGeoStudio as pgs
src_file = "../GeoStudio_files/Rapid drawdown.gsz" #specify the geostudio analyses file
geofile = pgs.GeoStudioFile(src_file) #open it with PyGeoStudio

# %%
# Materials defined in the study can be list with the ``showMaterials()`` method which show the material ID, their name and their types
geofile.showMaterials()

# %%
# More detail can be printing by manually getting the object:
mats = geofile["Materials"] #get material defined in the analysis
for mat in mats: #print the material name properties
  print(mat)
  print("----------------------")

# %%
# Below we selct the material nammed "Toe Drain", enter its hydraulic property and change its saturated hydraulic conductivity.
mat = geofile.getMaterialByName("Toe drain") #get material nammed "Toe drain"
mat["Hydraulic"]["KSat"] = 1e-6 #change its saturated permeability

# %%
# Note this is only for SatOnly material model.
# For SatUnsat material, users must change the relative hydraulic conductivity function directly, as for the "Dam fill" material:
mat2 = geofile.getMaterialByName("Dam fill") #get material nammed "Dam fill"
Krel = mat2["Hydraulic"]["KFn"]
print("Water suction:", Krel.getXData())
print("Hydraulic conductivity:", Krel.getYData())
new_Krel = Krel.getYData() * 10. # scale hydraulic conductivity by an order of magnitude
Krel.setYData(new_Krel)

# %%
# Modification can be saved under a new file
print("----------------------")
out_file = "./rapid_drawdown_changed_perm.gsz"
geofile.saveAs(out_file)
