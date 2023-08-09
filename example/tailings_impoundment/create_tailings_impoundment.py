import PyGeoStudio as pgs
import numpy as np

def simple_embankment(base_length, creek_length, height, base_coordinate=(0,0)):
    """
    Create a single embankment as:
    
       creek_length
           <->
           ___
          /   \         |
         /     \        |  height
    ____/_______\____   |
        <------->
       base_length
    
    The bottom left point is location can be specified with 
    base_coordinate (default: x=0, y=0).
    """
    points = np.array([
        [0, 0],
        [base_length, 0],
        [(base_length+creek_length)*0.5, height],
        [(base_length-creek_length)*0.5, height]
    ])
    points += np.array(base_coordinate)
    region = [0,1,2,3]
    return points, region



def multiple_embankment(embankment_specs, covering, base_coordinate=(0,0)):
    """
    Create multiple embankments as:
    
       base2
       <--->
       creek2
        <->
         __
        /  \      | height2
       /____\__   |
          /    \         |
         /      \        |  height1
    ____/________\____   |
           <-->
          creek1
        <-------->
           base1
    
    Multiple embankment spec are defined in a list of list, one list per embankment, such as for the above sketch:
    ``embankment_spec = [[base1,creek1,height1], [base2,creek2,height2]]``
    
    """
    all_points, region = simple_embankment(*embankment_specs[0])
    all_regions = [region]
    for i,spec in enumerate(embankment_specs[1:]):
        #add new points to the previous embankment if this embankment cover the previous
        if covering[i] != 0:
            original_point = np.copy(all_points[-1])
            all_points[-1,0] += covering[i]
            all_points = np.append(all_points, [original_point], axis=0)
            all_regions[-1] += [len(all_points)-1]
        #create new embankment
        points, region = simple_embankment(*spec)
        #move embankment
        points[:,0] += all_points[-1,0]-spec[0]+covering[i]
        points[:,1] += all_points[-1,1]
        #insert points and region
        region = [x+len(all_points) for x in region]
        region.insert(1,all_regions[-1][-1])
        all_points = np.append(all_points, points, axis=0)
        all_regions += [region]
    all_points += np.array(base_coordinate)
    return all_points, all_regions




if __name__ == "__main__":

  #open empty geostudio study
  src_file = "test.gsz" 
  geofile = pgs.GeoStudioFile(src_file,mode='r')
  geometry = geofile.getGeometry(1)
  
  #create the multiple embankment regions and vertices
  specs = [
      [20,13,7],
      [20,13,7],
      [10,5,5]
  ]
  covering = [2.,2.]
  base_coordinate = (100.,0.)
  points, regions = multiple_embankment(specs, covering, base_coordinate)
  
  #add new points
  new_ids = geometry.addPoints(points)
  new_ids = np.array(new_ids)
  #create new region
  for region in regions:
      pt_ids = new_ids[region]
      geometry.addRegion(pt_ids,)
  
  #show results
  geometry.showGeometry()
  
  #geofile.writeGeoStudioFile()
  
