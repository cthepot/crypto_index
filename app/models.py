from app import db, login, app
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assetname = db.Column(db.String(120), index=True, unique=True)
    slug = db.Column(db.String(48), index=True, unique=True)
    symbol = db.Column(db.String(10))
    is_active = db.Column(db.Boolean)
    rank = db.Column(db.Integer, unique=True)
    first_historical_data = db.Column(db.DateTime)
    last_historical_data = db.Column(db.DateTime)
    platform = db.Column(db.PickleType)
    id_cmc = db.Column(db.Integer, index=True, unique=True)
    quotes = db.relationship('Quote', backref='asset', lazy='dynamic')
    indexes = db.relationship('Index', secondary="index_asset")

    def __repr__(self):
        return u'<asset {}>'.format(self.assetname)

    # def __str__(self):
    # def __unicode___(self):


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cmc = db.Column(db.Integer, db.ForeignKey('asset.id_cmc'))
    assetname = db.Column(db.String(120), index=True)
    symbol = db.Column(db.String(10))
    slug = db.Column(db.String(48), index=True)
    num_market_pairs = db.Column(db.Integer, index=True)
    date_added = db.Column(db.DateTime)
    tags = db.Column(db.PickleType)
    max_supply = db.Column(db.Float)
    circulating_supply = db.Column(db.Float)
    total_supply = db.Column(db.Float)
    platform = db.Column(db.PickleType)
    price_usd = db.Column(db.Float)
    volume_24h_usd = db.Column(db.Float)
    percent_change_1h_usd = db.Column(db.Float)
    percent_change_24h_usd = db.Column(db.Float)
    percent_change_7d_usd = db.Column(db.Float)
    market_cap_usd = db.Column(db.Float)
    last_updated = db.Column(db.DateTime)

    def __repr__(self):
        return '<quote {}>'.format(self.assetname)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    baskets = db.relationship('Index', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Index(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(120))
    currency = db.Column(db.String(120))
    amount = db.Column(db.Integer)
    assets = relationship('Asset', secondary='index_asset')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Index {}>'.format(self.id)


class IndexAsset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id_cmc'))
    index_id = db.Column(db.Integer, db.ForeignKey('index.id'))
    asset = relationship(Asset, backref=backref("basket", cascade="all, delete-orphan"))
    index = relationship(Index, backref=backref("basket_item", cascade="all, delete-orphan"))
    allocation = db.Column(db.Float)
