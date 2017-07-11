from shapely.geometry import Polygon
from pprint import pprint
from models import mongo_collection, Node
import pickle, traceback, sys

from writeDB import db, NeigbhborhoodIndex

headers = ['forecast_pct','forecast_rent_pct','past_pct','past_rent_pct','rent_final_point','sale_rent_ratio','zestimate','market_health_index']

nodes_map = {}

with open('map.pickle', 'r') as inputfile:
  nodes_map = pickle.load(inputfile)

def growIndex(indexName, neighborhood, neighbors):
  if getattr(neighborhood, indexName) is not None:
    return
  
  nearest_values = []
  for n in neighbors:
    n_value = getattr(n, indexName)
    if n_value:
      n_value = float(n_value)
      nearest_values.append(n_value)
  if len(nearest_values) < float(len(neighbors))/2:
    print "Warning: not enough data for {} {}".format(neighborhood.name, nearest_values)
    return
  avg = reduce(lambda x, y: x + y, nearest_values) / len(nearest_values)
  print "{} of {} is {}".format(indexName, neighborhood.name, avg)
  setattr(neighborhood, indexName, avg)
  return True


def growIndexes(neighborhood, data_map, rounds, dryRun=True):
  record = nodes_map.get(neighborhood.regionid, None)
  if not record:
    print "Warning: neighborhood not in record {} {}".format(neighborhood.regionid, neighborhood.name)
    return False
  neighbors = [data_map.get(y) for y in [x.id for x in record.neighbors] if data_map.get(y) is not None]
  if len(neighbors) < 1:
    print "Warning: empty neighbors {} {}".format(neighborhood.regionid, neighborhood.name)
    return False
  growed = False
  for header in headers:
    if getattr(neighborhood, header) is not None:
      continue
    growed = growIndex(header, neighborhood, neighbors) or growed
  if growed:
    print "Saving neighborhood {}, {}".format(neighborhood.id, neighborhood.name)
    if not dryRun:
      neighborhood.growth_round = rounds
      neighborhood.save()
  return growed

def getNeighborhoodData(city):
  data_map = {}
  neighborhoods = NeigbhborhoodIndex.select().where(NeigbhborhoodIndex.city == city)
  for n in neighborhoods:
    data_map[n.regionid] = n
  return data_map

def growAllIndexes(dryRun=True):

  city_names = set([n.city for n in NeigbhborhoodIndex.select(NeigbhborhoodIndex.city).distinct()])
  for city in city_names:
    rounds = 0
    growing = True
    data_map = getNeighborhoodData(city)
    print "growing city {}".format(city)
    while growing:
      rounds += 1
      growing = False
      for neighborhood in data_map.values():
        growed = growIndexes(neighborhood, data_map, rounds, dryRun)
        if growed:
          growing = True
      print "round {} growing {}".format(rounds, growing)

if __name__ == "__main__":
  growAllIndexes(dryRun=False)




