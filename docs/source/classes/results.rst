.. _results:

Results
=======

Results of an analysis are accessed through under the Results property of the Analysis class:
To select a material nammed `Toe drain` for example:

.. code-block:: python

   #geofile is a GeoStudioFile instance
   geofile.showAnalysisTree()
   analysis1 = geofile.getAnalysisByID(1) 
   results1 = analysis1["Results"]

This will return an instance of the Results class which handle permit to import the results in Python.
Detail of the methods available are below:

.. autoclass:: PyGeoStudio.Results
    :members:

For example, to get the pore water pressure against time:

.. code-block:: python

    results1.getOutputVariables() #show available output variables
    locations = [[25,2],[23,1]] #get PWP at x=25,y=2 and x=23,y=1
    T,PWP = results1.getVariablesVsTime("PoreWaterPressure", locations=locations)
    fig,ax = plt.subplots()
    ax.plot(
      T, PWP,
      label=["x=25,y=2","x=23,y=1"]
    )
    ax.grid()
    ax.legend()
    ax.set_ylabel("PoreWaterPressure")
    ax.set_xlabel("Time (s)")
    plt.tight_layout()
    plt.show()

