from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Food:
    name: str
    api_uri: str
    price: float
    ordered: bool
    orderable: bool


@dataclass(frozen=True)
class Day:
    date: str
    foods: List[Food]
