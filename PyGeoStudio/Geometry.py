# This file is part of PyGeoStudio, an interface to GeoStudio 
# hydrogeotechnical software.
# Copyright (C) 2023, Moïse Rousseau
# 
# PyGeoStudio is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PyGeoStudio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET

# We do not use the BasePropertiesClass as there is too much specificities here.
# Or maybe the base class is not general enough ... ?

class Geometry:
  """
  :param Points: XY coordinates of the points in the geometry
  :type Points: numpy array
  :param Lines: List of lines in the geometry
  :type Lines: list
  :param Regions: List of regions in the geometry
  :type Regions: list
  :param MeshId: Index of the mesh associated with the geometry (do not change)
  :type MeshId: int
  :param Mesh: Mesh associated with the geometry
  :type Mesh: PyGeoStudio.Mesh object
  :param Name: Name of the geometry
  :type Name: str
  """
  def __init__(self):
    self.points = None
    self.lines = None
    self.mesh_id = None
    self.mesh = None
    self.name = None
    self.regions = {}
    self.other_elem = []
    return
  
  def __getitem__(self, parameter):
    match parameter:
      case "Points": return self.points
      case "Lines": return self.lines
      case "Regions": return self.regions
      case "MeshId": return None if self.mesh_id is None else int(self.mesh_id)
      case "Mesh": return self.mesh
      case "Name": return self.name
    return
  
  def draw(self, show=True):
    """
    Draw the geometry using matplotlib
    
    :param show: Show the figure (``True``, default) or plot it and show it latter (``False``)
    :type show: bool
    :return: Matplotlib figure and axis containing the plotted geometry
    :rtype: [fig,ax]
    """
    fig, ax = plt.subplots()
    #draw points
    ax.scatter(self.points[:,0], self.points[:,1], color='k')
    #draw lines
    for region in self.regions.values():
      region = region[0]
      for i in range(len(region)-1):
        X1, Y1 = self.points[region[i]-1]
        X2, Y2 = self.points[region[i+1]-1]
        ax.plot([X1,X2],[Y1,Y2], 'k')
      X1, Y1 = self.points[region[-1]-1]
      X2, Y2 = self.points[region[0]-1]
      ax.plot([X1,X2],[Y1,Y2], 'k')
    if show:
      plt.show()
    return fig,ax
  
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
          for x in region:
            other_attrib = []
            if x.tag == "ID":
              id_ = x.text
            if x.tag == "PointIDs":
              pts = [int(y) for y in x.text.split(',')]
            else:
              other_attrib.append(x)
          self.regions[f"Regions-{id_}"] = [pts, other_attrib]
      elif property_.tag == "MeshId":
        self.mesh_id = property_.text
      elif property_.tag == "ResultGraphs":
        pass #do not parse result graphics
      elif property_.tag == "Name":
        self.name = property_.text
      #elif property_.tag == "MeshDefaultEdgeLength":
      #  pass
      else:
        self.other_elem.append(property_)
    return
  
  def createRegion(self, pts):
    """
    Create new points, new lines and a region based on the point coordinates given.
    Must be given in order so they form a convex and non-intersecting polygon when joined successively.
    
    :param pts: The coordinate of the points to create a region
    :type pts: numpy array or list of list
    """
    n_pts_ini = len(self.points)
    self.add_points(pts)
    new_lines = [[x+n_pts_ini+1,x+n_pts_ini+2] for x in range(len(pts))]
    new_lines[-1][1] = n_pts_ini+1
    self.add_lines(new_lines)
    new_region = [x+n_pts_ini+1 for x in range(len(pts))]
    self.add_regions(new_region)
    return
  
  def addPoints(self, pts):
    """
    Add points to the geometry.
    
    :param pt: XY coordinates of the points
    :type pt: numpy array or list of list
    """
    self.points = np.append(self.points, pts)
    return
    
  def addLines(self, lines):
    """
    Add lines to the geometry.
    
    :param lines: Start-end indices of the points that form the lines
    :type lines: numpy array or list of list
    """
    self.lines = np.append(self.lines, new_lines)
    return
  
  def addRegions(self, pt_ids):
    """
    Create region with existing point given
    
    :param pt_ids: Indices of the point
    :type pt_ids: list of int
    """
    new_id = len(self.regions) + 1
    new_reg = [pt_ids, []]
    self.regions[f"Regions-{new_id}"] = new_reg
    return
  
  def __write__(self, et):
    #points
    sub = ET.SubElement(et, "Points")
    sub.attrib = {"Len":str(len(self.points))}
    for i,pt in enumerate(self.points):
      sub_pt = ET.SubElement(sub, "Point")
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
      for x in region[1]:
        sub_sub_reg = ET.SubElement(sub_reg, x.tag)
        sub_sub_reg.text = x.text
        sub_sub_reg.attrib = x.attrib
    #mesh id
    sub = ET.SubElement(et, "MeshId")
    sub.text = self.mesh_id
    #name
    sub = ET.SubElement(et, "Name")
    sub.text = self.name
    #others
    for prop in self.other_elem:
      et.append(prop)
    return

