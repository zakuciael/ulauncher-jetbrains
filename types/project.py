from typing import TypedDict, Optional
from ide_types import IdeKey


class Project(TypedDict, total=False):
    name: str
    path: str
    icon: Optional[str]
    score: int
    ide: IdeKey
