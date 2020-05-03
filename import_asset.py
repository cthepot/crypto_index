from app import db
from app.models import Asset, Quote
from app.quote import import_quote
import pandas as pd
import os
import csv
from pathlib import Path
from datetime import datetime



## Open and read the mapping document with csv without headers
map = list(csv.reader(open("cmc_get/output_map.csv")))


def convert_bool(raw):
    if raw == 1 or raw == "1": return True
    else: return False

def convert_date(self):
        try:
          date_split = self.split("T")
          date_days = date_split[0].split("-")
          date_time = date_split[1].split(":")
          date = date_days + date_time
          date = datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]))
          return date
        except:
          return None



## Manual test with hardcoded values
"""manual_test = Asset(
    id_cmc = 1,
    assetname = "test1",
    symbol = "test1",
    slug = "test1",
    is_active = True,
    rank = 1,
    first_historical_data = datetime(2013,4,28,18,47),
    last_historical_data = datetime(2013,4,28,18,47),
    platform = "test1")
db.session.add(manual_test)
print(manual_test)
db.session.commit()

## Manual test with the mappings
manual_test = Asset(
    id_cmc = int(map[1][0]),
    assetname = str(map[0][1]),
    symbol = str(map[0][2]),
    slug = str(map[0][3]),
    is_active = True,
    rank = int(map[1][5]),
    first_historical_data = convert_date(map[0][6]),
    last_historical_data = convert_date(map[0][7]),
    platform = map[0][8])
db.session.add(manual_test)
print(manual_test)
db.session.commit()"""

## Insert on the whole cmc mappings
for row in range(len(map)):
  u = Asset(
    id_cmc = int(map[row][0]),
    assetname = str(map[row][1]),
    symbol = str(map[row][2]),
    slug = str(map[row][3]),
    is_active = convert_bool(map[row][4]),
    rank = int(map[row][5]),
    first_historical_data = convert_date(map[row][6]),
    last_historical_data = convert_date(map[row][7]),
    platform = map[row][8])
  print(u, u.id_cmc, type(u.first_historical_data), type(u.last_historical_data), type(u.platform))
  db.session.add(u)
db.session.commit()
