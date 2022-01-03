"""
Ulauncher extension for opening recent projects on Jetbrains IDEs.
"""
import logging
import os
import re
from logging import WARN, INFO

import semver

from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.event import KeywordQueryEvent, PreferencesEvent, PreferencesUpdateEvent
from ulauncher.utils.decorator.debounce import debounce
from ulauncher.api.shared.Response import Response

from events.keyword_query_event import KeywordQueryEventListener
from events.preferences_event import PreferencesEventListener
from events.preferences_update_event import PreferencesUpdateEventListener

from utils.projects_parser import ProjectsParser
from utils.projects_list import ProjectsList

from typing_extensions import TYPE_CHECKING
from typing import Optional, TypedDict, cast, Match

if TYPE_CHECKING:
    from types.ide_types import IdeOptionsDict, IdeOptions, IdeKey, IdeAliases
    from types.project import Project


class JetbrainsLauncherExtension(Extension):
    """ Main Extension Class  """
    ides: 'IdeOptionsDict' = {
        "clion": {"name": "CLion", "config_prefix": "CLion", "launcher_prefix": "clion"},
        "idea": {"name": "IntelliJ IDEA", "config_prefix": "IntelliJIdea", "launcher_prefix": "idea"},
        "phpstorm": {"name": "PHPStorm", "config_prefix": "PHPStorm", "launcher_prefix": "phpstorm"},
        "pycharm": {"name": "PyCharm", "config_prefix": "PyCharm", "launcher_prefix": "pycharm"},
        "rider": {"name": "Rider", "config_prefix": "Rider", "launcher_prefix": "rider"},
        "webstorm": {"name": "WebStorm", "config_prefix": "WebStorm", "launcher_prefix": "webstorm"}
    }

    aliases: 'IdeAliases' = {}

    def __init__(self):
        """ Initializes the extension """
        super(JetbrainsLauncherExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateEventListener())

    @staticmethod
    def get_base_icon():
        """
        Returns the base (project) icon
        """

        path = os.path.join(os.path.dirname(__file__), "images", "icon.svg")
        if path is None or not os.path.isfile(path):
            raise FileNotFoundError(f"Cant find base icon")

        return path

    def parse_aliases(self, raw_aliases: str) -> list:
        """
        Parses raw aliases list into a python list
        :param raw_aliases: Raw aliases list
        """

        if raw_aliases is None:
            return []

        matches: list[tuple[str, 'IdeKey']] = re.findall(r"(\w+):(?: +|)(\w+)*;", raw_aliases)

        for alias, ide_key in matches:
            if self.check_ide_key(ide_key):
                self.aliases[alias] = ide_key
                self.logger.log(INFO, f"Added alias for ide key {ide_key}, value: {alias}")
            else:
                self.logger.log(WARN, f"Invalid ide key specified for alias {alias}. Expected one of {self.ides.keys()}")

    def check_ide_key(self, key: str) -> bool:
        """
        Checks if the provided key is an valid IDE key
        :param key: Key used to check validity
        :type key: str
        """

        return True if key in self.ides.keys() else False

    def get_ide_options(self, ide_key) -> 'IdeOptions | None':
        """
        Returns the IDE options
        :parm ide_key: The IDE key
        """

        if not self.check_ide_key(ide_key):
            raise AttributeError("Invalid ide key specified")

        return next((options for key, options in self.ides.items() if key == ide_key), None)

    def get_recent_projects(self, ide_key: 'IdeKey') -> list['Project']:
        """
        Returns the file path where the recent projects are stored
        :param ide_key: The IDE key
        """

        base_path = self.preferences.get("configs_path")
        if base_path is None or not os.path.isdir(os.path.expanduser(base_path)):
            raise AttributeError("Cant find configs directory")

        ide_options = self.get_ide_options(ide_key)
        if ide_options is None:
            raise AttributeError("Invalid ide key specified")

        configs: list[TypedDict("Config", {"path": str, "version": semver.VersionInfo})] = []
        for path in os.listdir(os.path.expanduser(base_path)):
            match = re.match(rf'^{ide_options.get("config_prefix")}(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)$', path)

            if match is not None:
                version_dict = {
                    key: 0 if value is None else value for key, value in match.groupdict().items()
                }

                configs.append({
                    "path": os.path.expanduser(os.path.join(base_path, path)),
                    "version": semver.VersionInfo(**version_dict)
                })

        if len(configs) == 0:
            return []

        config = max(configs, key=lambda conf: conf.get("version"))
        projects = ProjectsParser.parse(os.path.join(config.get("path"), "options", "recentProjects.xml"))

        for project in projects:
            project["ide"] = ide_key

        return projects

    def get_ide_icon(self, ide_key: 'IdeKey') -> str:
        """
        Returns the IDE icon
        :param ide_key: The IDE key
        """

        if not self.check_ide_key(ide_key):
            raise AttributeError("Invalid ide key specified")

        path = os.path.join(os.path.dirname(__file__), "images", f"{ide_key}.svg")
        if path is None or not os.path.isfile(path):
            raise FileNotFoundError(f"Cant find {ide_key} IDE icon")

        return path

    def get_ide_launcher_script(self, ide_key: 'IdeKey') -> str:
        """
        Returns the IDE launcher script path
        :param ide_key: The IDE key
        """

        scripts_path = self.preferences.get("scripts_path")
        if scripts_path is None or not os.path.isdir(os.path.expanduser(scripts_path)):
            raise AttributeError("Cant find shell scripts directory")

        ide_options = self.get_ide_options(ide_key)
        if ide_options is None:
            raise AttributeError("Invalid ide key specified")

        path = os.path.join(os.path.expanduser(scripts_path), ide_options.get("launcher_prefix"))
        if path is None or not os.path.isfile(path):
            raise FileNotFoundError(f"Cant find {ide_key} launcher script")

        return path

    @debounce(0.5)
    def handle_query(self, event: KeywordQueryEvent, query: str, ide_key: 'IdeKey | None') -> None:
        projects = ProjectsList(query, min_score=(60 if len(query) > 0 else 0), limit=8)

        if ide_key is not None:
            projects.extend(self.get_recent_projects(ide_key))
        else:
            for key in self.ides.keys():
                projects.extend(self.get_recent_projects(cast('IdeKey', key)))

        results = []

        try:
            if len(projects) == 0:
                results.append(
                    ExtensionResultItem(
                        icon=self.get_ide_icon(ide_key) if ide_key is not None else self.get_base_icon(),
                        name="No projects found",
                        on_enter=HideWindowAction()
                    )
                )
                return

            for project in projects:
                results.append(
                    ExtensionResultItem(
                        icon=project.get("icon") if project.get("icon") is not None else
                        self.get_ide_icon(project.get("ide")),
                        name=project.get("name"),
                        description=project.get("path"),
                        on_enter=RunScriptAction(
                            self.get_ide_launcher_script(project.get("ide")),
                            [project.get("path"), "&"]
                        ),
                        on_alt_enter=CopyToClipboardAction(project.get("path"))
                    )
                )
        finally:
            # Dirty way to send responses while using debouncing
            self._client.send(Response(event, RenderResultListAction(results)))


if __name__ == "__main__":
    JetbrainsLauncherExtension().run()
