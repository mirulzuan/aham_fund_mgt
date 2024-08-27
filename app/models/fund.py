from app.utils.db import db
from datetime import datetime
from sqlalchemy.dialects.mysql import CHAR

import uuid

class Fund(db.Model):
    __tablename__ = 'funds'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(CHAR(36), default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    fund_house = db.Column(db.String(255), nullable=False)
    nav = db.Column(db.Float, nullable=False)
    performance_percentage = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = db.Column(db.DateTime)

    def __init__(self, name, fund_house, nav, performance_percentage, description=None):
        self.name = name
        self.fund_house = fund_house
        self.nav = nav
        self.performance_percentage = performance_percentage
        self.description = description
    
    def __repr__(self):
        return f"<Fund {self.name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'fund_house': self.fund_house,
            'nav': self.nav,
            'performance_percentage': self.performance_percentage,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }
