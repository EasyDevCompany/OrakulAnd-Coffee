from datetime import datetime

from app.repository.users_limit import RepositoryUsersLimit
from app.repository.user import RepositoryTelegramUser


class UserLimitService:

    def __init__(
            self,
            repository_user_limit: RepositoryUsersLimit,
            repository_telegram_user: RepositoryTelegramUser
    ):
        self._repository_user_limit = repository_user_limit
        self._repository_telegram_user = repository_telegram_user

    async def create_limits(self, user_id: int):
        user = self._repository_telegram_user.get(user_id=user_id)
        users_limit = self._repository_user_limit.get(user_id=user_id)

        if not users_limit:
            return self._repository_user_limit.create(
                obj_in={"user_id": user_id, "user": user}
            )
        return users_limit

    async def update_limits(self, user_id: int):
        limit = self._repository_user_limit.get(user_id=user_id)
        card_count = limit.card_count + 1
        if card_count >= 3:
            return self._repository_user_limit.update(
                db_obj=limit,
                obj_in={"status": True, "users_block": datetime.now().date()},
                commit=True
            )
        return self._repository_user_limit.update(
            db_obj=limit,
            obj_in={"card_count": card_count},
            commit=True
        )

    def get_limit(self, user_id: int):
        return self._repository_user_limit.get(user_id=user_id)

    def reset_limits(self, user_id: int):
        return self._repository_user_limit.update(
            db_obj=self._repository_user_limit.get(user_id=user_id),
            obj_in={"status": False},
            commit=True
        )
