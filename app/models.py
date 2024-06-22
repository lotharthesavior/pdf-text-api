from datetime import datetime

from app.extensions import db
from typing import Optional
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

class Document(db.Model):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    unique_name: Mapped[str] = mapped_column(String(150), nullable=False)
    path: Mapped[str] = mapped_column(String(150), nullable=False)
    updated_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=False), default=datetime.utcnow, nullable=False
    )
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=False), onupdate=datetime.utcnow, default=datetime.utcnow, nullable=False
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'unique_name': self.unique_name,
            'path': self.path,
            'updated_at': self.updated_at,
            'created_at': self.created_at
        }

    def __repr__(self) -> str:
        return f'<Document {self.id}>'
