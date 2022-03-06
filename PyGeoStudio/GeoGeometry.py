import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET

class GeoStudioGeometry:
  def __init__(self):
    self.points = None
    self.lines = None
    self.regions = {}
    self.other_elem = []
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
        for region in property_:
          id_ = region[0].text
          pts = [int(x) for x in region[1].text.split(',')]
          mesh_attrib = region[2].attrib
          self.regions[f"Regions-{id_}"] = [pts, mesh_attrib]
      elif property_.tag == "MeshId":
        self.mesh_id = property_.text
      elif property_.tag == "ResultGraphs":
        pass #do not parse result graphics
      else:
        self.other_elem.append(property_)
    return
  
  def write(self, et):
    #points
    sub = ET.SubElement(et, "Points")
    sub.attrib = {"Len":str(len(self.points))}
    for i,pt in enumerate(self.points):
      sub_pt = ET.SubElement(et, "Point")
      sub_pt.attrib = {"ID":str(i+1), "X":str(pt[0]), 'Y':str(pt[1])}
    #lines
    sub = ET.SubElement(et, "Lines")
    sub.attrib = {"Len":str(len(self.lines))}
    for i,line in enumerate(self.lines):
      sub_line = ET.SubElement(sub, "Line")
      sub_sub_line = ET.SubElement(sub_line, "ID")
      sub_sub_line.text = str(i+1)
      sub_sub_line = ET.SubElement(sub_line, "PointID1")
      sub_sub_line.text = str(line[0]+1)
      sub_sub_line = ET.SubElement(sub_line, "PointID2")
      sub_sub_line.text = str(line[1]+1)
    #regions
    sub = ET.SubElement(et, "Regions")
    sub.attrib = {"Len":str(len(self.regions))}
    for id_,region in self.regions.items():
      sub_reg = ET.SubElement(sub, "Region")
      sub_sub_reg = ET.SubElement(sub_reg, "ID")
      sub_sub_reg.text = id_.split('-')[-1]
      sub_sub_reg = ET.SubElement(sub_reg, "PointIDs")
      sub_sub_reg.text = ','.join([str(x) for x in region[0]])
      sub_sub_reg = ET.SubElement(sub_reg, "Mesh")
      sub_sub_reg.attrib = region[1]
    #mesh id
    sub = ET.SubElement(et, "MeshId")
    sub.text = self.mesh_id
    #others
    for prop in self.other_elem:
      et.append(prop)
    return
    

