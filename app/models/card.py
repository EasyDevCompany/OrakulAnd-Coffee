from sqlalchemy import (
    String,
    Column,
    Integer
)
from app.db.base import Base


class Card(Base):
    __tablename__ = 'card'

    id = Column(Integer, primary_key=True)
    image = Column(String(50), default='')
    card_title = Column(String(50), default='')
    card_description = Column(String(2000), default='')

    def __str__(self):
        return f"{self.card_title}"
