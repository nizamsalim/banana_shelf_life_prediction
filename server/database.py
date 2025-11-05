from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SpoilageRecord(db.Model):
    __tablename__ = 'spoilage_records'

    id = db.Column(db.UUID, primary_key=True)
    stage = db.Column(db.String(8), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    ethylene = db.Column(db.Float, nullable=False)
    shelf_life_min = db.Column(db.Float)
    shelf_life_max = db.Column(db.Float)
    shelf_life_median = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'stage': self.stage,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'ethylene': self.ethylene,
            'shelf_life_min': self.shelf_life_min,
            'shelf_life_max': self.shelf_life_max,
            'shelf_life_median': self.shelf_life_median,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

