import matplotlib.colors as mcolors
import xml.etree.ElementTree as ET

class Color:
  """
  A helper class to handle color from GeoStudio file and Matplotlib colors.
  Color ojbect can be constructed either by specifying the name of a matplotlib color, or a list with RGB intensity from 0 to 255.
  """
  def __init__(self, arg):
    if isinstance(arg, ET.Element):
      self.rgb = [int(x) for x in arg.text.split("(")[-1][0:-1].split(',') ]
    elif isinstance(arg, str):
      self.setColor(arg)
    elif isinstance(arg, list):
      for x in arg:
        if len(arg) != 3:
          raise ValueError("List must have 3 elements for Red, Green and Blue intensity")
        if (not instance(x,int)) or (x<0 or x>255):
          raise ValueError("RGB color must me integer from 0 to 255 inclusive")
      self.rgb = arg
    else:
      raise ValueError(f"Can't set color from {arg}, try a nammed color from Matplotlib CSS4 colors (see `here <https://matplotlib.org/stable/gallery/color/named_colors.html#css-colors>`_) or with a RGB list.")
    return
  
  def setMPLColor(self, color):
    """
    Set color as defined in Matplotlib CSS4 colors (see `here <https://matplotlib.org/stable/gallery/color/named_colors.html#css-colors>`_).
    
    :param color: The color as defined in Matplotlib CSS4 colors
    :type color: str
    """
    self.rgb = [int(255*x) for x in mcolors.to_rgb(mcolors.CSS4_COLORS[color])]
    return
    
  def __str__(self):
    return "RGB Color = " + str(self.rgb)
  
  def __write__(self, et):
    text = f"RGB=({self.rgb[0]},{self.rgb[1]},{self.rgb[2]})"
    et.text = text
    return
      
