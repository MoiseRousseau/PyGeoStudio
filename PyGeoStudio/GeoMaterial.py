import xml.etree.ElementTree as ET

class GeoStudioMaterial:
  def __init__(self, geofile):
    self.id = None
    self.color = None
    self.name = None
    self.seep_model = None
    self.slope_model = None
    self.hydraulic_function = None
    self.stress_strain_model = None
    self.other_elem = []
    return
  
  def __str__(self):
    res = f"Material {self.name} (ID {self.id}, RGB color {self.color})\n"
    res += f"Seep model: {self.seep_model}\n"
    res += f"Hydraulic Function: {self.hydraulic_function}\n"
    res += f"Slope model: {self.slope_model}\n"
    res += f"Stress strain model parameter: {self.stress_strain_model}"
    if self.other_elem:
      res += f"\nOther properties (unsupported by PyGeoStudio):\n{self.other_elem}"
    return res
  
  def read(self, mat_):
    """
    Read material information contained in XML tree mat_
    """
    for prop in mat_:
      if prop.tag == "ID":
        self.id = int(prop.text)
      elif prop.tag == "Color":
        color = prop.text.split('(')[1][:-1]
        self.color = [int(x) for x in color.split(',')]
      elif prop.tag == "Name":
        self.name = prop.text
      elif prop.tag == "SeepModel":
        self.seep_model = prop.text
      elif prop.tag == "SlopeModel":
        self.slope_model = prop.text
      elif prop.tag == "Hydraulic":
        self.hydraulic_function = prop.attrib
      elif prop.tag == ("StressStrain"):
        self.stress_strain_model = {x.tag:x.text for x in prop}
      else:
        self.other_elem.append(prop)
    return
  
  def write(self, et):
    #ID
    sub = ET.SubElement(et, "ID")
    sub.text = str(self.id)
    #Color
    sub = ET.SubElement(et, "Color")
    sub.text = f"RGB=([{self.color[0]},{self.color[1]},{self.color[2]})"
    #Name
    sub = ET.SubElement(et, "Name")
    sub.text = str(self.name)
    #seep model
    sub = ET.SubElement(et, "SeepModel")
    sub.text = str(self.seep_model)
    #hydraulic function
    sub = ET.SubElement(et, "Hydraulic")
    sub.attrib = self.hydraulic_function
    #slope model
    sub = ET.SubElement(et, "SlopeModel")
    sub.text = str(self.slope_model)
    #strain model
    sub = ET.SubElement(et, "StressStrain")
    for tag,text in self.stress_strain_model.items():
      sub2 = ET.SubElement(et, tag)
      sub2.text = text
    for x in self.other_elem:
      et.append(x)
    return
