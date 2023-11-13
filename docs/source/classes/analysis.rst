.. _analysis:

Analysis
========

Analysis class holds the analysis properties, such as the geometry, the material distribution, the boundary conditions and the computational mesh if it is defined.

It can be accessed from the main driver ``GeoStudioFile`` with the method ``getAnalysisByName()`` or ``getAnalysisByID()``:

.. code-block:: python

   geofile.showAnalysisTree()
   analysis1 = geofile.getAnalysisByID(1) 

This will return an instance of the Analysis class which the user can access the properties described below.

.. autoclass:: PyGeoStudio.Analysis
    :members:
