from datetime import datetime, timedelta

from app.repository.user import RepositoryTelegramUser


class TelegramUserService:

    def __init__(self, repository_telegram_user: RepositoryTelegramUser):
        self._repository_telegram_user = repository_telegram_user

    async def create_user(self, user_id: int, username: str, first_name: str, last_name: str):
        user = self._repository_telegram_user.get(user_id=user_id)
        if not user:
            return self._repository_telegram_user.create(
                obj_in={
                    "user_id": user_id,
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name
                }
            )

        return user

    async def get_user_count(self):
        return self._repository_telegram_user.user_count()

    async def last_month_user(self):
        today = datetime.today().date()
        month_ago = today - timedelta(days=30)
        return self._repository_telegram_user.registration(
            today=today,
            reg_date=month_ago
        )

    async def last_week_user(self):
        today = datetime.today().date()
        week_ago = today - timedelta(days=7)
        return self._repository_telegram_user.registration(
            today=today,
            reg_date=week_ago
        )

    async def last_day_user(self):
        today = datetime.today().date()
        day_ago = today - timedelta(days=1)
        return self._repository_telegram_user.registration(
            today=today,
            reg_date=day_ago
        )

    async def list(self):
        return self._repository_telegram_user.list()

    def list_sync(self):
        return self._repository_telegram_user.list()
