from datetime import datetime
from sqlalchemy import (
    String,
    Column,
    Integer,
    BigInteger,
    DateTime,
    Boolean
)
from app.db.base import Base


class TelegramUser(Base):
    __tablename__ = 'telegram_user'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    username = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    registration_date = Column(DateTime, default=datetime.now().date())

    def __str__(self):
        return f"{self.last_name}"
