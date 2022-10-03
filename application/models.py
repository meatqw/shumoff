from application import db
from datetime import datetime, timedelta

# DB Model PRODUCT
class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    vendor = db.Column(db.String(200), nullable=True)
    title = db.Column(db.String(200), nullable=True)
    desc = db.Column(db.TEXT, nullable=True)
    attr = db.Column(db.TEXT, nullable=True)
    price = db.Column(db.Float(), nullable=True)
    size = db.Column(db.String(400), nullable=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())