from db import db
from pgvector.sqlalchemy import Vector
from sqlalchemy import func, Text, DateTime

class Embedding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    embedding = db.Column(Vector(1024), unique=True, nullable=False)
    text = db.Column(Text, unique=True, nullable=False)
    updated_at = db.Column(DateTime(timezone=False), server_default=func.current_timestamp(), nullable=False)
    created_at = db.Column(DateTime(timezone=False), onupdate=func.current_timestamp(), nullable=False)

    def __repr__(self):
        return f'<Embedding {self.id}>'
