from pymongo import MongoClient

class mongo_collection():
  def __init__(self, config):
    self.client = None
    self.config = config
  def __enter__(self):
    host, replicaSet, dbName, collectionName= self.config
    self.client = MongoClient(
        host,
        27017,
        replicaset=replicaSet,
        readPreference='secondaryPreferred'
    )
    return self.client
  def __exit__(self, *args):
    self.client.close()

class Node():
  def __init__(self, **kwargs):
    self.name = kwargs["name"]
    self.id = kwargs["id"]
    self.state = kwargs["state"]
    self.polygon = kwargs["polygon"]
    self.neighbors = kwargs.get("neighbors", [])
  def __str__(self):
    return "{} {} with {} neighbors {}".format(self.id, self.name, len(self.neighbors), str([x.name for x in self.neighbors]))
  __repr__ = __str__