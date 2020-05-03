from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pathlib import Path
import csv

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'2000',
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '8fdb0a0b-2f63-43a7-87b1-a5c634d1c023',
}

session = Session()
session.headers.update(headers)

try:
  #json load and differentiating status and data
  response = session.get(url, params=parameters)
  json = json.loads(response.text)
  status = json['status']
  data = json['data']
  print(status)

  #handling the output keys into one list for headers
  keys_list = list(data[0])
  quotes = ["price_usd" ,"volume_24h_usd","percent_change_1h_usd", "percent_change_24h_usd","percent_change_7d_usd","market_cap_usd","last_updated_usd" ]
  keys = keys_list[0:11] + quotes

  #opening file and writing keys as header
  w = csv.writer(open("output_quote.csv", "w"))
  w.writerow(keys)

  for i in range(len(data)):
    value_list = list(data[i].values())
    value_quote = list(data[i]["quote"]['USD'].values())
    value = value_list[0:11] + value_quote
    w.writerow(value)

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
