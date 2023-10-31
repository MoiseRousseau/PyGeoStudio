import plyfile
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import warnings


class Mesh:
  """
  Interface to the PLY mesh stored in the GeoStudio analysis
  
  :param [src_mesh]: Path to the mesh file in the GeoStudio archive
  :type [src_mesh]: src
  """
  def __init__(self, src_mesh):
    self.mesh = plyfile.PlyData.read(src_mesh)
    self.vertices = self.mesh.elements[1].data
    return
  
  def getMeshBoundingBox(self):
    """
    Return the two points of the diagonal of the mesh bounding box
    
    :return: Coordinate of the most bottom front left and most top rear right points of the mesh
    :rtype: list
    """
    min_point = [np.min(self.vertices['x']), np.min(self.vertices['y']), np.min(self.vertices['z'])]
    max_point = [np.max(self.vertices['x']), np.max(self.vertices['y']), np.max(self.vertices['z'])]
    return min_point, max_point
  
  def getPointIndexInMesh(self, location):
    """
    Return point index closest to the location given.
    
    :param [location]: [X,Y,Z] coordinate of the location
    :type [location]: Iterable
    :return: Index of the point in the mesh (0 based)
    :rtype: int
    """
    X,Y = location
    Z = 0.
    vertices = self.vertices
    domain_diag = (np.min(vertices['x'])-np.max(vertices['x']))**2 + \
                   (np.min(vertices['y'])-np.max(vertices['y']))**2 + \
                   (np.min(vertices['z'])-np.max(vertices['z']))**2 
    distance = (X-vertices['x'])**2 + \
                  (Y-vertices['y'])**2 + \
                  (Z-vertices['z'])**2
    champion = np.argmin(distance)
    if distance[champion] > 0.01 * domain_diag:
      warnings.warn(f"Warning, point {[X,Y,Z]} located at a relatively high distance from a mesh point: {np.sqrt(distance):.6e} / Domain bounding box diagonal {np.sqrt(domain_diag):.6e}", UserWarning)
    return champion
  
  def exportMesh(self, fmt):
    """
    Export the current mesh in the format provided for processing with another tools
    """
    return

