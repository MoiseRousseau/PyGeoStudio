import plyfile
import zipfile
import os
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt


class GeoStudioAnalysis:
  def __init__(self, geofile):
    self.geofile = geofile
    self.Index_in_xml = None
    self.ID = None
    self.Name = None
    self.Kind = None
    self.ParentID = None
    self.Method = None
    self.GeometryId = None
    self.ToSolve = None
    
    self.n_timestep = None
    self.timesteps = None
    self.saved_timesteps = None
    self.initialized = False
    return
  
  def getMeshBoundingBox(self):
    min_point = [np.min(self.vertices['x']), np.min(self.vertices['y']), np.min(self.vertices['z'])]
    max_point = [np.max(self.vertices['x']), np.max(self.vertices['y']), np.max(self.vertices['z'])]
    return min_point, max_point
  
  def getOutputVariables(self):
    saved_ts = np.argwhere(self.saved_timesteps == 1)[:,0]+1
    res = self.geofile.open(f"{self.Name.replace('/','&3')}/{saved_ts[0]:0>3d}/node.csv", 'r')
    header = res.readline().decode().rstrip().split(',')
    res.close()
    return header
  
  def showOutputVariables(self):
    saved_ts = np.argwhere(self.saved_timesteps == 1)[:,0]+1
    res = self.geofile.open(f"{self.Name.replace('/','&3')}/{saved_ts[0]:0>3d}/node.csv", 'r')
    header = res.readline().decode().rstrip().split(',')
    res.close()
    for x in header:
      print(x)
    return
  
  def getOutputTimes(self):
    return self.timesteps[self.saved_timesteps]
  
  def getPointIndexInResult(self, X,Y,Z):
    vertices = self.vertices
    domain_diag = (np.min(vertices['x'])-np.max(vertices['x']))**2 + \
                   (np.min(vertices['y'])-np.max(vertices['y']))**2 + \
                   (np.min(vertices['z'])-np.max(vertices['z']))**2 
    distance = (X-vertices['x'])**2 + \
                  (Y-vertices['y'])**2 + \
                  (Z-vertices['z'])**2
    champion = np.argmin(distance)
    if distance[champion] > 0.01 * domain_diag:
      print(f"Warning, point {[X,Y,Z]} located at high distance from a mesh point: {np.sqrt(distance):.6e} / Domain bounding box diagonal {np.sqrt(domain_diag):.6e}")
    print(champion+1, vertices[champion], distance[champion])
    return champion
    
  def getResults(self, variable, location=None):
    #check if variable is output and get its index
    try:
      variable_index = self.getOutputVariables().index(variable)
    except:
      print(f"Output variables \"{variable}\" not found in file")
      print("Available output variables are: ")
      self.showOutputVariables()
      raise
    saved_ts = np.argwhere(self.saved_timesteps == 1)[:,0]+1
    saved_time = self.getOutputTimes()
    if location is not None:
      if not isinstance(location, np.ndarray):
        if isinstance(location[0], list):
          location = np.array(location)
        else:
          location = np.array([location])
      n_location = len(location)
      champions = [0 for i in range(n_location)]
      for i in range(n_location):
        X,Y,Z = location[i]
        champions[i] = self.getPointIndexInResult(X,Y,Z)
    else:
      n_location = 0
#    if time is not None:
#      if isinstance(time,list) or isinstance(time,np.ndarray):
#        test = np.in1D(time, saved_time)
#        if len(test) != len(time): 
#          print("Some times requested are not available in the output times.")
#          print(f"Times found included: {test}")
#      elif isinstance(time,float) or isinstance(time,int):
#        pass
    datas = [None for i in saved_ts]
    temp = np.zeros(self.n_vertices, dtype='f8')
    for i,ts in enumerate(saved_ts):
      temp[:] = np.nan
      f = self.geofile.open(f"{self.Name.replace('/','&3')}/{ts:0>3d}/node.csv")
      data = np.genfromtxt(f, delimiter=',', skip_header=1)
      vertices_id = data[:,0].astype('i8')-1
      temp[vertices_id] = data[:,variable_index]
      if n_location:
        datas[i] = temp[champions]
      else:
        datas[i] = temp
      f.close()
    return saved_time,np.array(datas).transpose()
  
  def defineContext(self, x):
    self.context = x
    return
  
  def defineGeometry(self,x):
    self.geometry = x
    return
  
  def showProblem(self):
    fig,ax = self.geometry.drawGeometry()
    cmap = plt.get_cmap('tab20', np.max(self.context.material_distribution[:,1]))
    for reg, mat_id in self.context.material_distribution:
      pts = [x for x in self.geometry.regions[reg-1] if x!=-1]
      X_pts = [self.geometry.points[x,0] for x in pts]
      Y_pts = [self.geometry.points[x,1] for x in pts]
      ax.fill(X_pts, Y_pts,color=cmap(mat_id-1))
    plt.show()
    return
  
  def plotResults(self, var, location):
    if len(location)==2: location += [0.]
    t,y = self.getResults(var, location)
    fig,ax = plt.subplots()
    ax.plot(t,y[0],'r', label=var+" "+str(location))
    ax.grid()
    ax.legend()
    ax.set_ylabel(var)
    ax.set_xlabel("Time (s)")
    plt.tight_layout()
    plt.show()
    return
  
  def __initiate__(self):
    if self.initialized: return
    self.initialized = True
    #convert input to the right type
    if self.ID is not None: self.ID = int(self.ID)
    if self.ParentID is not None: self.ParentID = int(self.ParentID)
    if self.GeometryId is not None: self.GeometryId = int(self.GeometryId)
    #parse xml file to get analysis information
    xml = ET.parse(self.geofile.open(self.Name.replace('/','&3')+'/'+self.geofile.filename[:-3]+'xml'))
    root = xml.getroot()
    this_analysis = root[1][self.Index_in_xml]
    found = False
    for property_ in this_analysis:
      if property_.tag == "TimeIncrements": 
        found = True
        break
    if found:
      found = False
      for elem in property_:
        if elem.tag == "TimeSteps": 
          found = True
          break
    if found:
      self.n_timestep = int(elem.attrib["Len"])
      self.timesteps = np.zeros(self.n_timestep,dtype='f8')
      self.saved_timesteps = np.zeros(self.n_timestep,dtype='bool')
      for i,timestep in enumerate(elem):
        if "ElapsedTime" in timestep.attrib.keys():
          self.timesteps[i] = timestep.attrib["ElapsedTime"]
        if "Save" in timestep.attrib.keys(): 
          self.saved_timesteps[i] = True
    #get mesh information
    self.f_mesh = self.Name.replace('/','&3')+"/Mesh.ply"
    self.mesh = plyfile.PlyData.read(self.geofile.open(self.f_mesh))
    self.vertices = self.mesh.elements[1].data
    self.n_vertices = len(self.vertices)
    return  
