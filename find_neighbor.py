from shapely.geometry import Polygon
from pprint import pprint
from models import mongo_collection, Node
import pickle, traceback, sys

neighborhood_db = ('localhost', None, 'maps', 'neighborhoods')
nodes_map = {}

def getPolygons():
  polygons = []
  with mongo_collection(neighborhood_db) as neighborhood_client:
    neighborhood_coll = neighborhood_client[neighborhood_db[2]][neighborhood_db[3]]
    for neighborhood in neighborhood_coll.find():
      node = getPolygon(neighborhood)
      if node:
        polygons.append(node)
  return polygons

def getPolygon(neigh):
  regionID = neigh["properties"]["RegionID"]
  name = neigh["properties"]["Name"]
  coordinates = neigh["geometry"]["coordinates"]
  state = neigh["properties"]["State"]
  polygon = []
  # print regionID, name, coordinates[0], coordinates[-1]
  try:
    if neigh["geometry"]["type"] == "Polygon":
      coordinates = [tuple(x) for x in coordinates[0]]
      polygon = Polygon(coordinates[0:len(coordinates)-1])
    elif neigh["geometry"]["type"] == "MultiPolygon":
      tmp_polygons = []
      for tmp_coordinates in coordinates:
        proccessed_coordinates = [tuple(x) for x in tmp_coordinates[0]]
        polygon = Polygon(coordinates[0:len(proccessed_coordinates)-1])
        tmp_polygons.append(polygon)
      polygon = MultiPolygon(*tmp_polygons)
    else:
      print "Other type of polygons"
      exit(1)
      
  except Exception as e:
    # traceback.print_exc(file=sys.stdout)
    print "Error in {}".format(regionID)
    return None
  node = Node(id=regionID, name=name, polygon=polygon, state=state)
  return node

def getAja(polygons):
  global nodes_map
  counter = 0
  for i in xrange(len(polygons)):
    poly_a = polygons[i]
    for j in xrange(i+1, len(polygons)):
      poly_b = polygons[j]
      if poly_a.state != poly_b.state:
        continue
      adj = False
      if poly_a.polygon.touches(poly_b.polygon):
        adj = True
        # print "{} {} touches {} {}".format(poly_a.name, poly_a.id, poly_b.name, poly_b.id)
      if poly_a.polygon.intersects(poly_b.polygon):
        adj = True
        # print "{} {} intersects {} {}".format(poly_a.name, poly_a.id, poly_b.name, poly_b.id)
      if adj:
        if poly_a.id not in nodes_map:
          nodes_map[poly_a.id] = poly_a
        if poly_b.id not in nodes_map:
          nodes_map[poly_b.id] = poly_b
        node_a = nodes_map[poly_a.id]
        node_b = nodes_map[poly_b.id]
        if node_a != poly_a:
          print "warning: nodes with same ids {} {}".format(node_a, poly_a)
        if node_b != poly_b:
          print "warning: nodes with same ids {} {}".format(node_b, poly_b)
        node_a.neighbors.append(node_b)
        node_b.neighbors.append(node_a)
    counter += 1
    print("finished with {}, {} out of {}".format(poly_a.name, counter, len(polygons)))

if __name__ == "__main__":
  polygons = getPolygons()
  getAja(polygons)
  with open('map.pickle', 'w') as outputfile:
    pickle.dump(nodes_map, outputfile)
