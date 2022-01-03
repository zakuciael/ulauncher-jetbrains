from typing import Literal, TypedDict

IdeKey = Literal["clion", "idea", "phpstorm", "pycharm", "rider", "webstorm"]


class IdeOptions(TypedDict):
    name: str
    config_prefix: str
    launcher_prefix: str


IdeOptionsDict = [IdeKey, IdeOptions]
IdeAliases = dict[str, IdeKey]
