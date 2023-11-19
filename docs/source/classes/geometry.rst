.. _geometry:

Geometry
========

Geometry class interface geometry of the analysis.
There are binded to an Analysis object.
To access Geometry object:

.. code-block:: python

   geofile.showAnalysisTree()
   analysis1 = geofile.getAnalysisByID(1) 
   geom = analysis1["Geometry"]

Detail of the Geometry class:

.. autoclass:: PyGeoStudio.Geometry
    :members:
