.. _color:

Color
=====

Helper class to deal with color (support matplotlib defined colors).
To define a color (RGB defined or ``darkblue`` color from `matplotlib CCS4 color <https://matplotlib.org/stable/gallery/color/named_colors.html#css-colors>`_):

.. code-block:: python

   from PyGeoStudio import Color
   rgb_color = Color([156,35,76]) #RGB color
   darkblue_color = Color("darkblue") #matplotlib CSS4 color

To assign a color to a material nammed ``mat``:

.. code-block:: python

   mat["Color"] = darkblue_color

Detail of ``Color`` class:

.. autoclass:: PyGeoStudio.Color
    :members:
