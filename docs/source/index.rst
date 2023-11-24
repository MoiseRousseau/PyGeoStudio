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
     - OK
   * - Launch parametric study
     - OK
   * - Launch automatic calibration
     - TODO
   * - Launch sensitivity analysis with true design of experiment
     - TODO
   * - Uncertainty analysis through bayesian framework
     - TODO
   * - Create and duplication object
     - TODO
   * - Change analysis geometry (define points, lines, regions)
     - OK
   * - Change material distribution
     - OK
   * - Access and change hydraulic properties of materials
     - OK
   * - Access and change geotechnical properties of materials
     - Mohr-Coulomb model only
   * - Interface to functions (material and BC)
     - OK
   * - Interface to boundary conditions
     - TODO
   * - Access and change reinforcement properties
     - OK
   * - Access and change reinforcement geometries
     - TODO
   * - Access analysis results
     - SEEP only (experimental)
   * - Export results to Paraview (VTU format)
     - OK
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
   gallery_examples/index



Indices and tables
==================

* :ref:`genindex`

.. 
   * :ref:`modindex`
   * :ref:`search`

