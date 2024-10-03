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

By default, PyGeoStudio searches for the ``GeoCmd.exe`` executable in ``"C:/Program Files/Seequent/GeoStudio 20XX.Y/Bin"`` (i.e. in the default GeoStudio installation folder) and takes the latest version installed in case of multiple versions available.
If you install GeoStudio elsewhere, or what to use a specific version of GeoStudio, you must add the ``Bin`` folder in the system environment path.
Thus:

1. Search the location of the ``GeoCmd.exe`` executable.
2. Add this path in the system PATH variable as in this `WikiHow <https://www.wikihow.com/Change-the-PATH-Environment-Variable-on-Windows>`_
