""" Contains IdeData class """


# pylint: disable=too-few-public-methods
class IdeData:
    """ Class describing ide options"""
    name: str
    config_prefix: str
    launcher_prefix: str

    def __init__(self, name: str, config_prefix: str, launcher_prefix: str) -> None:
        super().__init__()
        self.name = name
        self.config_prefix = config_prefix
        self.launcher_prefix = launcher_prefix
