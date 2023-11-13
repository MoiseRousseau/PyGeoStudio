.. _reinforcement:

Reinforcement
=============

Reinforcement can be assessed through the Reinforcement class in PyGeoStudio. 
To select a reinforcement by its index for example:

.. code-block:: python

   #geofile is a GeoStudioFile instance
   geofile.showReinforcements()
   reinf = geofile.getReinforcementsByID(1) 

This will return an instance of the Reinforcement class which handle all the reinforcement properties.
Properties can be assessed with the ``[]`` operator and with the name of the property, for example:

.. code-block:: python
   
   f = reinf["PulloutResistance"] #store the pullout resistance in a variable
   reinf["PulloutResistance"] = 350 #change pullout resistance in-place


List of available properties:

.. autoclass:: PyGeoStudio.Reinforcement
    :members:
