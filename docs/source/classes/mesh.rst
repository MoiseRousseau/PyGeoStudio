.. _mesh:

Mesh
====

Meshes are accessed through the Geometry object:

.. code-block:: python

   analysis = geofile.getAnalysisByID(1)
   geom = analysis1["Geometry"]
   mesh = geom["Mesh"]

Detail of the mesh class:

.. autoclass:: PyGeoStudio.Mesh
    :members:
