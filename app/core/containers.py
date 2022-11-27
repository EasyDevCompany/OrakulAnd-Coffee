from dependency_injector import containers, providers

from app.repository.card import RepositoryCard
from app.repository.user import RepositoryTelegramUser
from app.repository.users_limit import RepositoryUsersLimit

from app.models.card import Card
from app.models.user import TelegramUser
from app.models.users_limits import UsersLimits

from app.services.telegram_user_service import TelegramUserService
from app.services.card_service import CardService
from app.services.users_limit_service import UserLimitService

from app.core.config import Settings


class Container(containers.DeclarativeContainer):

    config = providers.Singleton(Settings)

    repository_telegram_user = providers.Singleton(RepositoryTelegramUser, model=TelegramUser)
    repository_card = providers.Singleton(RepositoryCard, model=Card)
    repository_users_limits = providers.Singleton(RepositoryUsersLimit, model=UsersLimits)

    telegram_user_service = providers.Factory(TelegramUserService, repository_telegram_user=repository_telegram_user)
    users_limit_service = providers.Factory(
        UserLimitService,
        repository_user_limit=repository_users_limits,
        repository_telegram_user=repository_telegram_user
    )
    card_service = providers.Factory(CardService, repository_card=repository_card)



