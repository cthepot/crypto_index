import json
from sqlite3 import IntegrityError
from time import sleep
from threading import Thread
from app import app, db
from app.models import Asset, Quote
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime
from requests import Request, Session


class QuoteThread(Thread):
    def run(self):
        while True:
            sleep(app.config["SLEEP"])
            import_quote()


# function to convert date formats from get requests into datetime format
# please add seconds
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

# Get the mappings from CMC
def get_mapping():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    parameters = {
        'start': '1',
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': app.config["CMC_KEY"],
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        status = data['status']
        dataset = data['data']
        return dataset

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def import_mapping():
    mapping_cmc = get_mapping()
    mapping_psq = db.session.query(Asset.id_cmc).all()
    mapping_psq_list = []

    for ids in mapping_psq:
        mapping_psq_list.append(ids[0])






# Get the quotes from CMC
def get_quote():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {
        'start': '1',
        'limit': app.config["CMC_LIMIT"],
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': app.config["CMC_KEY"],
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        status = data['status']
        dataset = data['data']
        return dataset

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


# Import the quotes into the database
def import_quote():
    data = get_quote()
    quote_list = []

    for index in range(len(data)):
        if data[index]["quote"]["USD"]["volume_24h"] is None:
            data[index]["quote"]["USD"]["volume_24h"] = 0
        quote = Quote(id_cmc=int(data[index]["id"]),
                      assetname=data[index]["name"],
                      symbol=data[index]["symbol"],
                      slug=data[index]["slug"],
                      num_market_pairs=int(data[index]["num_market_pairs"]),
                      date_added=convert_date(data[index]["date_added"]),
                      tags=data[index]["tags"],
                      max_supply=data[index]["max_supply"],
                      circulating_supply=data[index]["circulating_supply"],
                      total_supply=data[index]["total_supply"],
                      platform=data[index]["platform"],
                      price_usd=float(data[index]["quote"]["USD"]["price"]),
                      volume_24h_usd=float(data[index]["quote"]["USD"]["volume_24h"]),
                      percent_change_1h_usd=float(data[index]["quote"]["USD"]["percent_change_1h"]),
                      percent_change_24h_usd=float(data[index]["quote"]["USD"]["percent_change_24h"]),
                      percent_change_7d_usd=float(data[index]["quote"]["USD"]["percent_change_7d"]),
                      market_cap_usd=float(data[index]["quote"]["USD"]["market_cap"]),
                      last_updated=convert_date(data[index]["quote"]["USD"]["last_updated"]))
        quote_list.append(quote)
        try:
            db.session.add(quote)
        except IntegrityError:
            print("is this happening")
    db.session.commit()
