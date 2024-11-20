""" Contains custom implementation of SortedList found in Ulauncher's code """
from typing import Iterator, List

from utils.SortedCollection import SortedCollection  # type: ignore
from utils.fuzzy_search import get_score  # type: ignore

from data.IdeProject import IdeProject


class ProjectsList:
    """
    List maintains items in a sorted order
    (sorted by a score, which is a similarity between item's name and a query)
    and limited to a number `limit` passed into the constructor
    """

    _query: str
    _min_score: int
    _limit: int
    _items: SortedCollection

    def __init__(self, query, min_score=30, limit=9) -> None:
        self._query = query.lower().strip()
        self._min_score = min_score
        self._limit = limit
        self._items = SortedCollection(
            key=lambda item:
            (-item.timestamp if item.timestamp is not None else 0)
            if not self._query else item.score
        )

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, i) -> IdeProject:
        return self._items[i]

    def __iter__(self) -> Iterator[IdeProject]:
        return iter(self._items)

    def __reversed__(self) -> Iterator[IdeProject]:
        return reversed(self._items)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}" + \
               f"({self._items}, min_score={self._min_score}, limit={self._limit})"

    def __contains__(self, item: IdeProject) -> bool:
        return item in self._items

    def extend(self, items: List[IdeProject]) -> None:
        """
        Merges all provided items into this list
        :param items: A list of items to merge
        """
        for item in items:
            self.append(item)

    def append(self, item: IdeProject) -> None:
        """
        Adds item to the list
        :param item: Item to add
        """
        name = item.name
        path = item.path.replace(r"^~", "")

        if not self._query:
            self._items.insert(item)

            while len(self._items) > self._limit:
                self._items.pop()
        else:
            score = max(get_score(self._query, name), get_score(self._query, path))

            if score >= self._min_score:
                # use negative to sort by score in desc. order
                item.score = -score

                self._items.insert(item)
                while len(self._items) > self._limit:
                    # remove items with the lowest score to maintain limited number of items
                    self._items.pop()
