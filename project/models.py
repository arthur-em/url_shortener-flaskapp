from project import db
from datetime import datetime


class Url(db.Model):
    """
    Class that represents the urls that will be shortened. 
    """

    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    original_url = db.Column(db.String, nullable=False)
    clicks = db.Column(db.Integer, nullable=False, default=0)
