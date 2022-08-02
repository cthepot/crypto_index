# Cryptocurrency index fund

As an authentified user, create a basket of cryptocurrency from CMC list and track its performance. Limited front-end, unfinished.

## Start

    $ cd crypto_index
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip3 install -r requirements.txt
    $ export FLASK_app="cif.py"
    $ export DATABASE_URL="postgresql:///cif_db"
    $ flask run


## Debug mode

$ export FLASK_DEBUG=1
