from typing import Any, Callable, Iterator

from sqlalchemy.orm import Query
from sqlalchemy.orm.interfaces import MapperOption


class CustomIter(MapperOption):
    def __init__(self, iter_strategy: Callable[[Query], Iterator[Any]]):
        self.custom_iter = iter_strategy

    def process_query(self, query) -> None:
        query.custom_iter = self.custom_iter
