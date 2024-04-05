""" Contains IdeData class """
from __future__ import annotations

from typing import List


# pylint: disable=too-few-public-methods
class IdeData:
    """ Class describing ide options"""
    name: str
    config_prefixes: [str]
    launcher_prefixes: List[str]
    custom_config_key: str | None
    recent_projects_file: str

    def __init__(self, name: str, config_prefixes: [str], launcher_prefixes: List[str],
                 custom_config_key: str | None = None, recent_projects_file: str = "recentProjects.xml") -> None:
        super().__init__()
        self.name = name
        self.config_prefixes = config_prefixes
        self.launcher_prefixes = launcher_prefixes
        self.custom_config_key = custom_config_key
        self.recent_projects_file = recent_projects_file
