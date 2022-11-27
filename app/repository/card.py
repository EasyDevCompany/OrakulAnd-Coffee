from .base import RepositoryBase

from app.models.card import Card


class RepositoryCard(RepositoryBase[Card]):
    pass
