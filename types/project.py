""" Contains project type """

from typing import TypedDict, Optional

from types.ide_types import IdeKey


class Project(TypedDict, total=False):
    """ Dictionary describing project data """
    name: str
    path: str
    icon: Optional[str]
    score: int
    ide: IdeKey
