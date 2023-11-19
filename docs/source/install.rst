.. _installation:


Installation
============

Installing Python
-----------------

PyGeoStudio is written in pure Python 3 language which should be installed first.
For Linux and MacOS user, Python is already available on your system.
For Windows user, go on `Python website <https://www.python.org/>`_ to download and install the Python programming language.
Python version 3.10 and superior is recommanded.


Installing PyGeoStudio
----------------------

Once Python is installed, PyGeoStudio can be installed using the ``pip`` package manager.
To do so, `open a Powershell interpretor <https://www.howtogeek.com/662611/9-ways-to-open-powershell-in-windows-10/>`_ and type:

.. code-block::

    pip install PyGeoStudio


Make PyGeoStudio recognize GeoStudio
------------------------------------

In order to call GeoStudio solver from Python, PyGeoStudio must know where is GeoStudio installed.
By default, PyGeoStudio searches for executable in ``"C:/Program Files/Seequent/GeoStudio 2023.1"`` (i.e. in the default GeoStudio installation folder).
If you install GeoStudio elsewhere, you must set that folder by opening the Python console (through Idle) or using the PowerShell interpretor (command ``python``) and typing:

.. code-block:: python

    import PyGeoStudio as pgs
    pgs.defineGeoStudioLauncher("C:/Program Files/Seequent/GeoStudio 2023.1")
    exit()


Replace the string ``"C:/Program Files/Seequent/GeoStudio 2023.1"`` by your path to GeoStudio and correct the version if necessary.
Note this is a one time action.
Once set, the path will be stored in the library for future call.
The change takes effect after the next import of PyGeoStudio.
This means you can't set the path to GeoStudio in the same script that is doing calculations.
