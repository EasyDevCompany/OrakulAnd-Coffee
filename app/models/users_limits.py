from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean,
    ForeignKey
)
from app.db.base import Base
from sqlalchemy.orm import relationship


class UsersLimits(Base):
    __tablename__ = "users_limits"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey('telegram_user.user_id')
        )
    card_count = Column(Integer, default=0)
    users_block = Column(DateTime, default=None, nullable=True)
    status = Column(Boolean, default=False)
    user = relationship("TelegramUser")

    def __str__(self):
        return f"{self.user_id}"