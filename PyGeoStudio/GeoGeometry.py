import matplotlib.pyplot as plt
import numpy as np

class GeoStudioGeometry:
  def __init__(self, geofile):
    self.geofile = geofile
    self.points = None
    self.lines = None
    self.regions = None
    return
  
  def drawGeometry(self):
    fig, ax = plt.subplots()
    for line in self.lines:
      X1, Y1 = self.points[line[0]]
      X2, Y2 = self.points[line[1]]
      ax.plot([X1,X2],[Y1,Y2], 'k')
    return fig,ax
  
  def showGeometry(self):
    fig,ax = self.drawGeometry()
    plt.show()
    return
  
  def read(self, element):
    for property_ in element:
      if property_.tag == "Points":
        self.points = np.zeros((int(property_.attrib["Len"]),2),dtype='f8')
        for point in property_:
          self.points[int(point.attrib["ID"])-1] = [float(point.attrib["X"]), float(point.attrib["Y"])]
      elif property_.tag == "Lines":
        self.lines = np.zeros((int(property_.attrib["Len"]),2),dtype='i8')-1
        for line in property_:
          self.lines[int(line[0].text)-1] = [int(line[1].text)-1,int(line[2].text)-1]
      elif property_.tag == "Regions":
        self.regions = np.zeros((int(property_.attrib["Len"]),99),dtype='i8')-1
        for region in property_:
          id_ = int(region[0].text)-1
          pts = [int(x)-1 for x in region[1].text.split(',')]
          pts += [-1 for x in range(99-len(pts))]
          self.regions[int(region[0].text)-1] = pts
      elif property_.tag == "MeshId":
        self.mesh_id = property_.text
      else:
        setattr(self, property_.tag, property_.text)
    return
    

