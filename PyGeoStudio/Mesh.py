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

import plyfile
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import warnings


class Mesh:
  """
  :param MeshId: Index of the mesh
  :type MeshId: int
  :param Vertices: XY coordinates of mesh vertices
  :type Vertices: numpy array
  :param Elements: list of mesh vertices defining the mesh elements
  :type Elements: list
  """
  def __init__(self, mesh_id, src_mesh):
    self.mesh_id = mesh_id
    self.mesh = plyfile.PlyData.read(src_mesh)
    self.vertices = self.mesh['node']
    self.elements = self.mesh['element']['id']
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
    
    :param location: [X,Y,Z] coordinate of the location
    :type location: Iterable
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
  
  def asMeshIOData(self):
    """
    Convert Mesh data into MeshIO format points and cells: 
    
    .. code-block:: python
    
        points, cells = mesh_study.getMeshIOData()
        meshio_object = MeshIO.Mesh(points=points, cells=cells)
    
    :return: Points and Cells in MeshIO suitable format.
    :rtype: numpy array, list
    """
    x = self.vertices['x']
    y = self.vertices['y']
    z = self.vertices['z']
    points = np.array([x,y,z]).transpose()
    cells = [
      ("triangle", [x-1 for x in self.elements if len(x) == 3]),
      ("quad", [x-1 for x in self.elements if len(x) == 4])
    ]
    return points, cells

  def write(self, path):
    """
    Extract and save the mesh in GeoStudio native format with extention ``.ply``
    
    :param path: Path to the output mesh file
    :type path: str
    """
    self.mesh.write(path)
    self.mesh.write("test.ply")
    return
  
  def export(self, path, point_data=None):
    """
    Export the current mesh with point data provided in another format. Export are carried with MeshIO.
    
    :param path: Path to the output mesh file
    :type path: str
    :param point_data: Point data to write with the mesh (default = No data). Supplied as a dictionary with point dataset name as the key and value a iterable whose size match the number of point in the mesh.
    :type point_data: dict
    """
    try:
      import meshio
    except:
      raise RuntimeError("Please install MeshIO to use this capability")
    points, cells = self.asMeshIOData()
    mesh = meshio.Mesh(
      points,
      cells,
      point_data=point_data,
    )
    mesh.write(path)
    return

