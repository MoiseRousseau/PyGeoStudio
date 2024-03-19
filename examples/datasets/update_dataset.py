"""
Working with datasets
=====================

"""

# %%
# This example shows how to interact with datasets.
# We first import PyGeoStudio and open the study
import PyGeoStudio as pgs
import numpy as np

src_file = "../GeoStudio_files/Soil Cover Modeling - Hydraulic Response.gsz"
geofile = pgs.GeoStudioFile(src_file)

# %% 
# Dataset are defined for all analyses in the study and can be retrieven directly from the GeoStudio study in ``geofile``
geofile.showDatasets()
dataset = geofile.getDatasetByName("Daily Precipitation")
print("\n", dataset)

# %%
# Data contained in a data can be accessed with the ``"Data"`` attribute which is a NumPy array
# For example, changing precipitation for the third data row (at time T = 3 days)
dataset["Data"][2,1] = 1e-9 # m/d
print("\nDataset after changing first row: ", dataset)

# %%
# Dataset can be created from scratch by supplying a array:
new_dataset = geofile.createNewDataset("MyNewDataset",["Time","WaterFlux"])
arr = np.arange(0,46).reshape(23,2).astype(float) #create a example array
new_dataset.loadDataFromArray(arr)
print("\nNew dataset: ", new_dataset)

# %%
# Or by reading a file
csv_dataset = geofile.createNewDataset("MyNewCSVDataset",["Time","WaterFlux"])
csv_dataset.loadDataFromCSV("./adataset.csv")
print("\nCSV dataset: ", csv_dataset)
geofile.saveAs("modified_datasets.gsz")
