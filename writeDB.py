import csv
import peewee
from peewee import *

db = MySQLDatabase('data', user='root')

class NeigbhborhoodIndex(peewee.Model):
  name = peewee.CharField(null = True)
  regionid = peewee.CharField(null = True)
  city = peewee.CharField(null = True)
  city_area = peewee.CharField(null = True)
  state = peewee.CharField(null = True)
  forecast_pct = peewee.FloatField(null = True)
  forecast_rent_pct = peewee.FloatField(null = True)
  past_pct = peewee.FloatField(null = True)
  past_rent_pct = peewee.FloatField(null = True)
  rent_final_point = peewee.FloatField(null = True)
  sale_rent_ratio = peewee.FloatField(null = True)
  zestimate = peewee.FloatField(null = True)
  market_health_index = peewee.FloatField(null = True)
  growth_round = peewee.IntegerField(null = True)

  class Meta:
    database = db
    db_table = 'n_index'

headers = ['name','regionid','city','city_area','state','forecast_pct','forecast_rent_pct',' past_pct','past_rent_pct','rent_final_point','sale_rent_ratio','zestimate','market_health_index']

def perform(dryRun=False):
  with open('data.csv', 'r') as csvfile:
    bulk = 1000
    counter = 0
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    data_source = []
    for row in reader:
      # neighborhood = NeigbhborhoodIndex(**row)
      data_source.append(row)
      if len(data_source) >= bulk:
        with db.atomic():
          counter += 1
          print "Inserting batch {}".format(counter)
          if not dryRun:
            NeigbhborhoodIndex.insert_many(data_source).execute()
        data_source = []

if __name__ == "__main__":
  NeigbhborhoodIndex.create_table()
  # perform()
