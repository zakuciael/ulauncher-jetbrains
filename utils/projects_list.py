""" Contains custom implementation of SortedList found in Ulauncher's code """

from typing_extensions import TYPE_CHECKING
from ulauncher.utils.SortedCollection import SortedCollection
from ulauncher.utils.fuzzy_search import get_score

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from types.project import Project


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
        self._items = SortedCollection(key=lambda item: item.get("score"))

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, i) -> 'Project':
        return self._items[i]

    def __iter__(self) -> 'iter(Project)':
        return iter(self._items)

    def __reversed__(self) -> 'reversed[Project]':
        return reversed(self._items)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}" + \
               f"({self._items}, min_score={self._min_score}, limit={self._limit})"

    def __contains__(self, item) -> bool:
        return item in self._items

    def extend(self, items: 'list[Project]') -> None:
        """
        Merges all provided items into this list
        :param items: A list of items to merge
        """
        for item in items:
            self.append(item)

    def append(self, item: 'Project') -> None:
        """
        Adds item to the list
        :param item: Item to add
        """
        name = item.get("name")
        path = item.get("path").replace(r"^~", "")

        score = max(get_score(self._query, name), get_score(self._query, path))

        if score >= self._min_score:
            # use negative to sort by score in desc. order
            item["score"] = -score

            self._items.insert(item)
            while len(self._items) > self._limit:
                # remove items with the lowest score to maintain limited number of items
                self._items.pop()
