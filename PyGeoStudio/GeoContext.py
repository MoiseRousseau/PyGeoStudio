import numpy as np

class GeoStudioContext:
  def __init__(self, geofile):
    self.geofile = geofile
    self.material_distribution = None
    self.analysisID = None
    return
  
  def __str__(self):
    return 
  
  def read(self, element):
    for property_ in element:
      if property_.tag == "GeometryUsesMaterials":
        self.material_distribution = np.zeros((int(property_.attrib["Len"]),2), dtype='i8')-1
        for i,mat in enumerate(property_):
          reg = int(mat.attrib["ID"].split('-')[-1])
          mat_id = int(mat.attrib["Entry"])
          self.material_distribution[i] = [reg,mat_id]
      if property_.tag == "AnalysisID":
        self.analysisID = int(property_.text)
    return
