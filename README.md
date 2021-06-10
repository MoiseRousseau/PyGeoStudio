# PyGeoStudio

Python library allowing reading/writing GeoStudio .gsz file. 
But, why do you need an external software such as Python to read your file while GeoStudio possess graphical tool to create your analysis and visualize your data ?

1. Automatise your numerical model processing without the need to export it in Excel
2. Harness the power of Python to treat your data
3. Make quality plots using [matplotlib](www.matplotlib.org)
4. Modify analysis without using the graphical interface
5. Program analysis (e.g. the same analysis but with different parameters)
6. Perform automatic calibration / optimisation
7. The idea you have in might which is not included in the 6 before

## Features

Below is the implemented (and tested) features:

* Read (and write in the futur) GeoStudio file containing
* Draw the conceptual model created in GeoStudio
* Read analysis results and extract temporal and spatial data
* Plot analysis results at given coordinates

## Getting started

`PyGeoStudio` library will be further installable through the `pip` command.
For instance, just download the repository and copy the `PyGeoStudio` folder where you create your Python script (which could be the folder containing your GeoStudio file, or not)
You will need to install the following Python library: `matplotlib`, `numpy`

## Examples

One example is provided in the folder `example`. 
It contains the `rapid_drawdown` tutorial problem found on GeoStudio website.
In this example, `PyGeoStudio` is used to plot the overall problem and to plot the evolution of the pore wwater pressure at a given point. 

## Roadmap

* Improve reading
* Implement writing (to modify the input file)
* Solve analysis directly in Python
* Loop over input - solve - output to allow optimization
* Other examples

## Contributing

Every contribution is welcome!
Note this is a brand new project for me, and that I develop the library based on my need.
If you have a particular problem with GeoStudio you want to solve with Python, just let me know, and I would figure out what I can do to help you.

If you like this project, please star it! 
It will encourage me to pursuit its development.


