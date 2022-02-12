""" Contains project type """
from __future__ import annotations

from data.IdeKey import IdeKey


# pylint: disable=too-few-public-methods
class IdeProject:
    """ Dictionary describing project data """
    name: str
    ide: IdeKey
    path: str
    timestamp: int | None
    icon: str | None
    score: int

    # pylint: disable=too-many-arguments
    def __init__(self, name: str, ide: IdeKey, path: str,
                 timestamp: int | None, icon: str | None = None) -> None:
        super().__init__()

        self.name = name
        self.ide = ide
        self.path = path
        self.timestamp = timestamp
        self.icon = icon
        self.score = 0
