.. _class_material:


Material properties
===================

Material properties can be assessed through the Material class in PyGeoStudio. 
To select a material nammed `Toe drain` for example:

.. code-block:: python

   #geofile is a GeoStudioFile instance
   geofile.showMaterials()
   mat = geofile.getMaterialByName("Toe drain") #get material nammed "Toe drain" as a Material instance

This will return an instance of the Material class which handle all the material properties.
List of available properties are described in the subsection below.


Material
--------

Properties can be assessed with the ``[]`` operator and with the name of the property, for example:

.. code-block:: python
   
   seepmodel = mat["SeepModel"] #store seep model (SatOnly or SatUnsat) in a variable
   mat["SeepModel"] = "SatUnsat" #change seep model to SatUnsat

List of properties:

.. autoclass:: PyGeoStudio.Material
    :members:


Hydraulic Properties
--------------------

Accessed through the `Hydraulic` property of the Material class:

.. code-block:: python

   hydraulic_props = mat["Hydraulic"]

Example using and changing the saturated hydraulic conductivity:

.. code-block:: python

   KSat = hydraulic_props["KSat"] #get
   geotech_props["KSat"] = 1e-6   #set

List of properties:

.. autoclass:: PyGeoStudio.Material.MaterialHydraulicFunction


Geotechnical properties
-----------------------

Accessed through the `StressStrain` property of the Material class:

.. code-block:: python

   geotech_props = mat["StressStrain"]


Example using and changing the unit weight:

.. code-block:: python
   
   mat_unit_weight = geotech_props["UnitWeight"] #get
   geotech_props["UnitWeight"] = 20.3 #set

List of properties:

.. autoclass:: PyGeoStudio.Material.MaterialStressStrain
