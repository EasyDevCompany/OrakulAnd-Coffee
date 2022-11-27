from .base import RepositoryBase

from app.models.user import TelegramUser
from sqlalchemy import func


class RepositoryTelegramUser(RepositoryBase[TelegramUser]):

    def user_count(self):
        return self._session.query(func.count(self._model.id)).first()

    def registration(self, today, reg_date):
        return self._session.query(self._model).filter(
            self._model.registration_date <= today,
            self._model.registration_date >= reg_date
        ).all()