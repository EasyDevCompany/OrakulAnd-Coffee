from .base import RepositoryBase

from app.models.users_limits import UsersLimits


class RepositoryUsersLimit(RepositoryBase[UsersLimits]):
    pass