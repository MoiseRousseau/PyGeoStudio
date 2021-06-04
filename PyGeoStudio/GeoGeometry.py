import matplotlib.pyplot as plt

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
    

