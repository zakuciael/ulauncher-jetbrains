""" Contains IdeData class """
from __future__ import annotations

from typing import List


# pylint: disable=too-few-public-methods
class IdeData:
    """ Class describing ide options"""
    name: str
    config_prefix: str
    launcher_prefixes: List[str]
    custom_config_key: str | None

    def __init__(self, name: str, config_prefix: str, launcher_prefixes: List[str],
                 custom_config_key: str | None = None) -> None:
        super().__init__()
        self.name = name
        self.config_prefix = config_prefix
        self.launcher_prefixes = launcher_prefixes
        self.custom_config_key = custom_config_key
