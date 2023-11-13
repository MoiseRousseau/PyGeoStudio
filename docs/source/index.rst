.. PyGeoStudio documentation master file, created by
   sphinx-quickstart on Tue Oct 17 20:53:21 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyGeoStudio's documentation!
=======================================

PyGeoStudio is a library that interface the Hydrogeotechnical software suite GeoStudio with Python.
It allows to open, modify, and write back a study so user can automate their modelling with Python scripting.

Note PyGeoStudio is not made to design study from scratch.
It rather permits to modify existing study without the need of the graphical interface and couple with other Python library.


Features
--------

.. list-table:: Implemented and planned features (not exhaustive)
   :widths: auto
   :header-rows: 1

   * - Feature
     - Status
   * - Open GeoStudio File
     - OK
   * - Write (possibly modified) GeoStudio File
     - OK
   * - Launch GeoStudio through Python
     - TODO
   * - Change analysis geometry (define points, lines, regions)
     - OK
   * - Change material distribution
     - OK
   * - Access and change hydraulic properties of materials
     - Saturated only
   * - Access and change geotechnical properties of materials
     - Mohr-Coulomb model only
   * - Interface to functions (such as unsaturated properties)
     - TODO
   * - Interface to boundary conditions
     - TODO
   * - Access and change reinforcement properties
     - OK
   * - Access and change reinforcement geometries
     - TODO
   * - Access analysis results
     - SEEP only (experimental)
   * - Export result to Paraview (more advanced post-processing)
     - TODO
   * - Access meshes
     - Partial (experimental)
   * - Import meshes
     - TODO
   * - Meshing with external tool
     - TODO

 

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   install.rst
   user_guide.rst



Indices and tables
==================

* :ref:`genindex`

.. 
   * :ref:`modindex`
   * :ref:`search`

