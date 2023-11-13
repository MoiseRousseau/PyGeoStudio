.. _class_geostudiofile:


Main driver GeoStudioFile
=========================

Main driver for opening a GeoStudio file and accessing properties of a study:

.. code-block:: python

    import PyGeoStudio as pgs
    src_file = "Reinforcement with Anchors.gsz"
    geofile = pgs.GeoStudioFile(src_file,mode='r')

The following method are callable using for example:

.. code-block:: python

    geofile.showMaterials() #show a list of materials
    geofile.getMaterialByID(3) #return material with ID 3

Description the availables methods to interact with the study:

.. autoclass:: PyGeoStudio.GeoStudioFile
    :members:
