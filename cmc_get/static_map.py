from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pathlib import Path
import csv

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
parameters = {
  'start':'1',
  #'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '8fdb0a0b-2f63-43a7-87b1-a5c634d1c023',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  json = json.loads(response.text)
  status = json['status']
  data = json['data']
  keys = data[0].keys()

  w = csv.writer(open("output_map.csv", "w"))
  w.writerow(keys)

  for i in range(len(data)):
    value = data[i].values()
    w.writerow(value)


except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
