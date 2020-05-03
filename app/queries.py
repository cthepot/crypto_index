from app import app, db
from app.models import Asset, Quote, Index, IndexAsset, User
from sqlalchemy import func, and_


sq = db.session.query(Quote.assetname, db.func.max(Quote.last_updated).label("latest_updated")).group_by(Quote.assetname).subquery()

latest_quotes = db.session.query(sq.c.assetname, sq.c.latest_updated, Quote.price_usd,
                                Quote.market_cap_usd, Quote.percent_change_24h_usd, Quote.id_cmc.label("id_cmc"), Quote.symbol)\
        .join(Quote, and_(Quote.assetname == sq.c.assetname, Quote.last_updated == sq.c.latest_updated))\
        .order_by(Quote.market_cap_usd.desc())\
        .group_by(sq.c.assetname, sq.c.latest_updated, Quote.price_usd, Quote.market_cap_usd, Quote.percent_change_24h_usd, Quote.id_cmc, Quote.symbol)