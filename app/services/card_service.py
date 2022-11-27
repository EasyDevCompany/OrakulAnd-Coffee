from random import randint
from app.repository.card import RepositoryCard


class CardService:

    def __init__(self, repository_card: RepositoryCard):
        self._repository_card = repository_card

    async def add_card(
            self,
            image: str,
            card_title: str,
            card_description: str
    ):
        return self._repository_card.create(
            obj_in={
                "image": image,
                "card_title": card_title,
                "card_description": card_description
            }
        )

    async def get_card(self):
        ransom_num = randint(0, 20)
        return self._repository_card.get(
            id=ransom_num
        )
