from application import db
from datetime import datetime

# DB Model PRODUCT
class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    vendor = db.Column(db.String(200), nullable=True)
    title = db.Column(db.String(200), nullable=True)
    desc = db.Column(db.TEXT, nullable=True)
    attr = db.Column(db.TEXT, nullable=True)
    price = db.Column(db.Float(), nullable=True)
    size = db.Column(db.String(400), nullable=True)
    type = db.Column(db.String(400), nullable=True)
    link = db.Column(db.String(400), nullable=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())

# DB Model BODY
class Body(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    effect_max = db.Column(db.JSON, nullable=True)
    effect_great = db.Column(db.JSON, nullable=True)
    effect_good = db.Column(db.JSON, nullable=True)
    effect_practical = db.Column(db.JSON, nullable=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())
    
# DB Model Auto
class Auto(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    brand = db.Column(db.String(200), nullable=True)
    model = db.Column(db.String(200), nullable=True)
    body = db.Column(db.Integer(), db.ForeignKey('body.id'), nullable=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())