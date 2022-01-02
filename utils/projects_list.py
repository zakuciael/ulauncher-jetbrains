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

    def __init__(self, query, min_score=30, limit=9):
        self._query = query.lower().strip()
        self._min_score = min_score
        self._limit = limit
        self._items = SortedCollection(key=lambda item: item.get("score"))

    def __len__(self):
        return len(self._items)

    def __getitem__(self, i):
        return self._items[i]

    def __iter__(self):
        return iter(self._items)

    def __reversed__(self):
        return reversed(self._items)

    def __repr__(self):
        return '%s(%r, min_score=%s, limit=%s)' % (
            self.__class__.__name__,
            self._items,
            self._min_score,
            self._limit
        )

    def __contains__(self, item):
        return item in self._items

    def extend(self, items):
        for item in items:
            self.append(item)

    def append(self, project: 'Project'):
        name = project.get("name")
        path = project.get("path").replace(r"^~", "")

        score = max(get_score(self._query, name), get_score(self._query, path))

        if score >= self._min_score:
            project["score"] = -score  # use negative to sort by score in desc. order
            self._items.insert(project)
            while len(self._items) > self._limit:
                self._items.pop()  # remove items with the lowest score to maintain limited number of items
