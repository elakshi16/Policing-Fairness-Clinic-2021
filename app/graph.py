import fiona
from shapely.geometry import shape, mapping, Point, Polygon, MultiPolygon
from shapely.ops import unary_union

import pandas as pd
import numpy as np
import matplotlib
import math as math
import pickle

R_EARTH = 6371 * 1000
DATA_PATH = "./data"

####################
# Helper functions #
####################
def add_lat(latitude, change):
  return (latitude  + (change / R_EARTH) * (180 / math.pi))

def add_lon(longitude, change, max_lat):
  return (longitude + (change / R_EARTH) * (180 / math.pi) / math.cos(max_lat * 180/math.pi))

##############
# Node class #
##############
class Node:
  def __init__(self, node_ID, bound_box, records, pop=0):
    self.ID = node_ID
    self.bounds = bound_box
    self.center_lat = (bound_box['min_lat'] + bound_box['max_lat']) / 2
    self.center_lon = (bound_box['min_lon'] + bound_box['max_lon']) / 2
    self.pd_reports = records
    self.population = pop

  def __repr__(self):
    return(f"id: {self.ID} , @({self.center_lat},{self.center_lon}), report_cnt = {len(self.pd_reports)}")

class Graph:
  def __init__(self, bound_size=150, data_path= DATA_PATH + '/Los_Angeles_Crime_Data_from_2020_to_Present.csv'):
    self.nodes = {}
    self.tracts = {}
    self.bound_size = 150

    # import and clean arrest dataset
    self.arrest_dataset = pd.read_csv(data_path)
    self.arrest_dataset.rename({'LON': 'Longitude', 'LAT': 'Latitude', 'DR_NO': 'Incident Tag', 'Crm Cd Desc': 'Crime Desc'}, axis=1, inplace=True)
    self.arrest_dataset.insert(loc=0, column='ID', value=np.arange(len(self.arrest_dataset)))
    self.arrest_dataset.set_index('ID', inplace=True)

    self.arrest_datasum = self.arrest_dataset[['Incident Tag', 'Longitude', 'Latitude', 'Crime Desc']]

  def createNodes(self, from_file = False, save_file = False, shp_path = DATA_PATH + '/LAPD_Divisions/LAPD_Divisions.shp'):
    if (from_file):
        # Check if File exists
        in_file = open(from_file, 'rb')
        self.nodes = pickle.load(in_file)
        print("loaded nodes from pickle")
    else :
      # Create bounding box
      min_lon= 180.0
      max_lon= -180.0
      min_lat= 90.0
      max_lat= -90.0
      for index, row in self.arrest_datasum.iterrows():
        longitude= float(row[1])
        latitude= float(row[2])
        if (longitude == 0.0 or latitude ==0.0):
          continue
        min_lon = min(min_lon, longitude)
        max_lon = max(max_lon, longitude)
        min_lat = min(min_lat, latitude)
        max_lat = max(max_lat, latitude)
        
      latitude = min_lat
      longitude = min_lon
      change = self.bound_size

      self.bound_coords = {'min_lon':min_lon, 'min_lat':min_lat, 'max_lon':max_lon, 'max_lat':max_lat}

      # get boundary of LA  
      layer = fiona.open(shp_path)
      precincts = [shape(geom['geometry']) for geom in layer]
      LA_union = unary_union(precincts)

      # create grid of nodes
      y_ind = 0
      while latitude < self.bound_coords['max_lat']:
        longitude = self.bound_coords['min_lon']
        new_lat = add_lat(latitude, self.bound_size)
        x_ind = 0

        while longitude < self.bound_coords['max_lon']:
          new_lon = add_lon(longitude, self.bound_size, self.bound_coords['max_lat'])

          matches = self.arrest_datasum[(self.arrest_dataset.Latitude < new_lat) & (self.arrest_dataset.Latitude > latitude) & (self.arrest_dataset.Longitude < new_lon) & (self.arrest_dataset.Longitude > longitude)]
          bnd_box = {'min_lat':latitude, 'max_lat':new_lat, 'min_lon':longitude, 'max_lon':new_lon}

          n = Node((x_ind, y_ind), bnd_box, matches)
          pt = Point(n.center_lon, n.center_lat)
          # only add nodes inside LA
          if pt.within(LA_union):
            self.nodes[(x_ind, y_ind)] = n  

          x_ind += 1
          longitude = new_lon
        
        y_ind += 1
        latitude = new_lat
        print(f"Finished row: {y_ind}")

      if save_file:
        self.saveNodes(save_file)


  def populateNodes(self):
      tracts_layer = fiona.open(DATA_PATH + "/Demographic_Data/Census_Tracts_2010_Population/Census_Tracts_2010_Population.shp")
      LA_layer = fiona.open(DATA_PATH + "/LAPD_Divisions/LAPD_Divisions.shp")

      LA_city_polygon = unary_union([shape(precinct['geometry']) for precinct in LA_layer])

      # Select tracts contained in LA
      la_tracts = {}
      for tract in tracts_layer:
        tract_polygon = shape(tract['geometry'])
        if tract_polygon.within(LA_city_polygon):
          tract_properties = tract['properties']
          la_tracts[tract_properties['TRACTCE10']] = ([], tract_properties, tract_polygon)

      tracts_dict = la_tracts
      
      # Assign nodes to tracts
      tract_nodes = {}
      for node_id, node in self.nodes.items():
        for tract_name, (node_list, tract_prop, tract_pol) in tracts_dict.items():
          pt = Point(node.center_lon, node.center_lat)
          if pt.within(tract_pol):
            node_list.append(node_id)

      # Set Node Populations
      for tract_name, (node_list, properties, pol) in tracts_dict.items():  
        tnodes = node_list
        totNodes = len(tnodes) 
        for node in tnodes:
          self.nodes[node].population = (properties['POP'] // totNodes)
      
      self.tracts = tracts_dict

    

  def getNeighbors(self, node):
    neighbors = []
    x,y = node.ID
    opts = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]

    for pair in opts:
      if pair in self.nodes.keys():
        neighbors += pair

    return neighbors
  

  def saveNodes(self, file_path):
    pickle_out = open(file_path, 'a+')
    pickle.dump(self.nodes, pickle_out)
    pickle_out.close()
    print("Saved pickle nodes")