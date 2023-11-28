"""
Change reinforcement properties
===============================

"""

# %%
# This example shows how to list, select and interact with reinforcements
# We first import PyGeoStudio and open the study `Reinforcement with Anchors <https://www.geoslope.com/learning/support-resources/example-files/example?id=examples:slopew:reinforcementwithanchors&resourceVersion=11.1.0.00000>`_ from GeoStudio website:
import PyGeoStudio as pgs
src_file = "../GeoStudio_files/Reinforcement with Anchors.gsz"
geofile = pgs.GeoStudioFile(src_file) #open it with PyGeoStudio

# %%
# Reinforcements defined in the study can be list with the ``showReinforcements()`` method which shows the reinforcement ID, their name and their type:
geofile.showReinforcements()

# %%
# More detail can be printing by manually getting the object:
reinfs = geofile["Reinforcements"] #get reinforcements defined in the study
for reinf in reinfs: #print the reinforcement properties
  print(reinf)
  print("----------------------")

# %%
# Once selected by name with ``getReinforcementByName()`` method or by their ID with ``getReinforcementByID()``, properties such as the pullout resistance can be changed with:
reinf1 = geofile.getReinforcementByName("New Reinforcement")
reinf1 = geofile.getReinforcementByID(1)
reinf1["PulloutResistance"] = 350

# %%
# Modification to reinforcement need to be save in a new file with
out_file = "./Reinforcement_with_Anchors_modified.gsz"
geofile.saveAs(out_file)
