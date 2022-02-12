""" Ulauncher extension for opening recent projects on Jetbrains IDEs. """
from __future__ import annotations

import os
import re
from typing import Dict, cast

import semver
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent, PreferencesEvent, PreferencesUpdateEvent

from data.IdeData import IdeData
from data.IdeKey import IdeKey
from data.IdeProject import IdeProject
from events.KeywordQueryEventListener import KeywordQueryEventListener
from events.PreferencesEventListener import PreferencesEventListener
from events.PreferencesUpdateEventListener import PreferencesUpdateEventListener
from utils.RecentProjectsParser import RecentProjectsParser


class JetbrainsLauncherExtension(Extension):
    """ Main Extension Class  """
    ides: Dict[IdeKey, IdeData] = {
        "clion": IdeData(name="CLion", config_prefix="CLion", launcher_prefixes=["clion"]),
        "idea": IdeData(name="IntelliJ IDEA", config_prefix="IntelliJIdea",
                        launcher_prefixes=["idea"]),
        "phpstorm": IdeData(name="PHPStorm", config_prefix="PHPStorm",
                            launcher_prefixes=["phpstorm"]),
        "pycharm": IdeData(name="PyCharm", config_prefix="PyCharm",
                           launcher_prefixes=["pycharm", "charm"]),
        "rider": IdeData(name="Rider", config_prefix="Rider", launcher_prefixes=["rider"]),
        "webstorm": IdeData(name="WebStorm", config_prefix="WebStorm",
                            launcher_prefixes=["webstorm"]),
        "goland": IdeData(name="GoLand", config_prefix="GoLand", launcher_prefixes=["goland"]),
        "datagrip": IdeData(name="DataGrip", config_prefix="DataGrip",
                            launcher_prefixes=["datagrip"]),
        "rubymine": IdeData(name="RubyMine", config_prefix="RubyMine",
                            launcher_prefixes=["rubymine"]),
        "android-studio": IdeData(name="Android Studio", config_prefix="AndroidStudio",
                                  launcher_prefixes=["studio"],
                                  custom_config_key="studio_config_path")
    }

    aliases: Dict[str, IdeKey] = {}

    def __init__(self):
        """ Initializes the extension """
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateEventListener())

    @staticmethod
    def get_base_icon():
        """
        Returns the base (project) icon
        :return: None
        """

        path = os.path.join(os.path.dirname(__file__), "images", "icon.svg")
        if path is None or not os.path.isfile(path):
            raise FileNotFoundError("Cant find base icon")

        return path

    def parse_aliases(self, raw_aliases: str) -> None:
        """
        Parses raw aliases list into a python list
        :param raw_aliases: Raw aliases list
        """

        if raw_aliases is None:
            return

        matches = re.findall(r"(\w+):(?: +|)([\w-]+)*;", raw_aliases)

        for alias, ide_key in matches:
            if self.check_ide_key(ide_key):
                self.aliases[alias] = cast(IdeKey, ide_key)
                self.logger.info("Loaded alias: %s -> %s", ide_key, alias)
            else:
                self.logger.warning(
                    "Invalid ide key specified for alias %s. Expected one of %s",
                    alias, ", ".join(self.ides.keys()))

    def check_ide_key(self, key: str) -> bool:
        """
        Checks if the provided key is valid
        :param key: Key to check
        :return: Result of the check
        """

        return key in self.ides

    def get_ide_data(self, ide_key: IdeKey) -> IdeData | None:
        """
        Gets IDE data for specified key
        :parm ide_key: IDE key
        :return: IDE data
        """

        if not self.check_ide_key(ide_key):
            raise AttributeError("Invalid ide key specified")

        return next((ide_data for key, ide_data in self.ides.items() if key == ide_key), None)

    def get_recent_projects(self, ide_key: IdeKey) -> list[IdeProject]:
        """
        Get parsed recent projects for specified key
        :param ide_key: IDE key
        :return: Parsed recent projects
        """

        ide_data = self.get_ide_data(ide_key)
        if ide_data is None:
            raise AttributeError("Invalid ide key specified")

        base_path = os.path.expanduser(
            self.preferences.get(ide_data.custom_config_key) \
                if ide_data.custom_config_key else self.preferences.get("configs_path")
        )
        if base_path is None or not os.path.isdir(base_path):
            raise FileNotFoundError("Cant find configs directory")

        versions: list[semver.VersionInfo] = []
        for path in os.listdir(base_path):
            match = re.match(
                f"^{ide_data.config_prefix}" +
                r"(?P<major>0|[1-9]\d*)(\.(?P<minor>0|[1-9]\d*)(\.(?P<patch>0|[1-9]\d*))?)?",
                path)

            if match is not None:
                version_dict = {
                    key: 0 if value is None else value for key, value in match.groupdict().items()
                }

                versions.append(semver.VersionInfo(**version_dict))

        if len(versions) == 0:
            return []

        version = max(versions)
        config_dir = os.path.join(
            base_path,
            f"{ide_data.config_prefix}{version.major}.{version.minor}",
            "options"
        )

        projects = RecentProjectsParser.parse(
            os.path.join(config_dir, "recentProjects.xml"),
            ide_key
        )

        if ide_key == "rider":
            projects += RecentProjectsParser.parse(
                os.path.join(config_dir, "recentSolutions.xml"),
                ide_key
            )

        return projects

    def get_ide_icon(self, ide_key: IdeKey) -> str:
        """
        Gets path to the IDE icon for specified key
        :param ide_key: IDE key
        :return: Path to the IDE icon
        """

        if not self.check_ide_key(ide_key):
            raise AttributeError("Invalid ide key specified")

        path = os.path.join(os.path.dirname(__file__), "images", f"{ide_key}.svg")
        if path is None or not os.path.isfile(path):
            raise FileNotFoundError(f"Cant find {ide_key} IDE icon")

        return path

    def get_ide_launcher_script(self, ide_key: IdeKey) -> str | None:
        """
        Gets path to the IDE launcher script for specified key
        :param ide_key: IDE key
        :return: Path to the IDE launcher script
        """

        scripts_path = self.preferences.get("scripts_path")
        if scripts_path is None or not os.path.isdir(os.path.expanduser(scripts_path)):
            raise AttributeError("Cant find shell scripts directory")

        ide_data = self.get_ide_data(ide_key)
        if ide_data is None:
            raise AttributeError("Invalid ide key specified")

        for prefix in ide_data.launcher_prefixes:
            path = os.path.join(os.path.expanduser(scripts_path), prefix)
            if path is not None and os.path.isfile(path):
                return path

        return None


if __name__ == "__main__":
    JetbrainsLauncherExtension().run()
