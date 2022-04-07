from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Food:
    name: str
    api_uri: str
    # TODO: add these xD
    # price: int
    #locked: bool = False
    #ordered: bool = False

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'api_uri': self.api_uri
        }


@dataclass(frozen=True)
class DayMenu:
    day: str
    foods: List[Food]

    def to_dict(self) -> dict:
        return {
            'day': self.day,
            'foods': list(map(lambda x: x.to_dict(), self.foods))
        }


@dataclass(frozen=True)
class MonthMenu:
    days: List[DayMenu]

    def to_dict(self) -> dict:
        return {
            'days': list(map(lambda x: x.to_dict(), self.days)),
        }
