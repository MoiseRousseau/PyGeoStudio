
class GeoStudioMaterial:
  def __init__(self, geofile):
    self.id = None
    self.color = None
    self.name = None
    self.seep_model = None
    self.slope_model = None
    self.hydraulic_function = None
    self.stress_strain_model = None
    return
  
  def __str__(self):
    res = f"Material {self.name} (ID {self.id})\n"
    res += f"Seep model: {self.seep_model}\n"
    res += f"Hydraulic Function: {self.hydraulic_function}\n"
    res += f"Slope model: {self.slope_model}\n"
    res += f"Stress strain model parameter: {self.stress_strain_model}"
    return res
  
  def read(self, mat_):
    """
    Read material information contained in XML tree mat_
    """
    self.id = int(mat_.find("ID").text)
    color = mat_.find("Color").text.split('(')[1][:-1]
    self.color = [float(x)/256 for x in color.split(',')]
    self.name = mat_.find("Name").text
    self.seep_model = mat_.find("SeepModel").text
    self.slope_model = mat_.find("SlopeModel").text
    self.hydraulic_function = mat_.find("Hydraulic").attrib
    model_ = mat_.find("StressStrain")
    self.stress_strain_model = {x.tag:x.text for x in model_}
