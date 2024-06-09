from app import db
from typing import Optional
from sqlalchemy import String, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

class Document(db.Model):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    path: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    updated_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=False), server_default=func.current_timestamp(), nullable=False
    )
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=False), onupdate=func.current_timestamp(), nullable=False
    )

    def __repr__(self) -> str:
        return f'<Document {self.id}>'
