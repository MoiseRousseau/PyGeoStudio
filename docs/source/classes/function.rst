.. _function:

Function
========

Interface through the custom function in the study, such as water retention curves, hydraulic function, custom boundary conditions or reinforcements.

To print and select a function defined in the GeoStudio study ``geofile``:

.. code-block:: python

   geofile.showFunctions()
   krel = geofile.getFunctionByName("Silty clay K function")


Function can be also assessed directly from a material object:

.. code-block:: python

   mat = geofile.getMaterialByName("Dam fill")
   krel = mat["KFn"]

Details of ``Function`` class:

.. autoclass:: PyGeoStudio.Function
    :members:
