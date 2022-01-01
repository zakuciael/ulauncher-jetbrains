"""
Ulauncher extension for opening recent projects on Jetbrains IDEs.
"""
import os
import re
import semver

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.Response import Response

from jetbrains.projects_parser import ProjectsParser
from ulauncher.utils.decorator.debounce import debounce


class JetbrainsLauncherExtension(Extension):
    """ Main Extension Class  """
    ides = {
        "clion": {"name": "CLion", "config_prefix": "CLion", "launcher_prefix": "clion"},
        "idea": {"name": "IntelliJ IDEA", "config_prefix": "IntelliJIdea", "launcher_prefix": "idea"},
        "phpstorm": {"name": "PHPStorm", "config_prefix": "PHPStorm", "launcher_prefix": "phpstorm"},
        "pycharm": {"name": "PyCharm", "config_prefix": "PyCharm", "launcher_prefix": "pycharm"},
        "rider": {"name": "Rider", "config_prefix": "Rider", "launcher_prefix": "rider"},
        "webstorm": {"name": "WebStorm", "config_prefix": "WebStorm", "launcher_prefix": "webstorm"}
    }

    def __init__(self):
        """ Initializes the extension """
        super(JetbrainsLauncherExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

    @staticmethod
    def get_base_icon():
        """
        Returns the base (project) icon
        """

        path = os.path.join(os.path.dirname(__file__), "images", "icon.svg")
        if path is None or not os.path.isfile(path):
            raise FileNotFoundError(f"Cant find base icon")

        return path

    def check_ide_key(self, key):
        """
        Checks if the provided key is an valid IDE key
        @param str key: Key used to check validity
        """

        return True if key in self.ides.keys() else False

    def get_ide_options(self, ide_key):
        """
        Returns the IDE options
        @parm str ide_key: The IDE key
        """

        if not self.check_ide_key(ide_key):
            raise AttributeError("Invalid ide key specified")

        return next((options for key, options in self.ides.items() if key == ide_key), None)

    def get_recent_projects(self, ide_key):
        """
        Returns the file path where the recent projects are stored
        @param str ide_key: The IDE key
        """

        base_path = self.preferences.get("configs_path")
        if base_path is None or not os.path.isdir(os.path.expanduser(base_path)):
            raise AttributeError("Cant find configs directory")

        ide_options = self.get_ide_options(ide_key)
        if ide_options is None:
            raise AttributeError("Invalid ide key specified")

        configs = []
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

    def get_ide_icon(self, ide_key):
        """
        Returns the IDE icon
        @param str ide_key: The IDE key
        """

        if not self.check_ide_key(ide_key):
            raise AttributeError("Invalid ide key specified")

        path = os.path.join(os.path.dirname(__file__), "images", f"{ide_key}.svg")
        if path is None or not os.path.isfile(path):
            raise FileNotFoundError(f"Cant find {ide_key} IDE icon")

        return path

    def get_ide_launcher_script(self, ide_key):
        """
        Returns the IDE launcher script path
        @param str ide_key: The IDE key
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
    def handle_query(self, event, args, ide_key=None):
        query = " ".join(args)

        print(f"Query: {query}")
        print(f"IDE Key: {ide_key}")

        projects = []

        if ide_key is not None:
            projects = self.get_recent_projects(ide_key)
        else:
            for key in self.ides.keys():
                projects = projects + self.get_recent_projects(key)

        items = []
        
        try:
            if len(projects) == 0:
                items.append(
                    ExtensionResultItem(
                        icon=self.get_ide_icon(ide_key) if ide_key is not None else self.get_base_icon(),
                        name="No projects found",
                        on_enter=HideWindowAction()
                    )
                )
                return

            for project in projects[:8]:
                items.append(
                    ExtensionResultItem(
                        icon=project.get("icon") if project.get("icon") is not None else
                        self.get_ide_icon(project.get("ide")),
                        name=project.get("name"),
                        description=os.path.join("~", os.path.relpath(project.get("path"), os.path.expanduser("~"))),
                        on_enter=RunScriptAction(
                            self.get_ide_launcher_script(project.get("ide")),
                            [project.get("path"), "&"]
                        ),
                        on_alt_enter=CopyToClipboardAction(project.get("path"))
                    )
                )
        finally:
            # Dirty way to send responses while using debouncing
            self._client.send(Response(event, RenderResultListAction(items)))


class KeywordQueryEventListener(EventListener):
    """ Listener that handles the user input """

    def on_event(self, event, extension):
        """
        Handles the keyword event
        @param KeywordQueryEvent event: Event object
        @param JetbrainsLauncherExtension extension: Extension object
        """

        args = [arg.lower() for arg in re.split("[ /]+", (event.get_argument() or ""))]
        ide_key = args[0] if extension.check_ide_key((args[0] if len(args) > 0 else "")) else None
        args = args[1:] if ide_key is not None else args

        extension.handle_query(event, args, ide_key)


if __name__ == "__main__":
    JetbrainsLauncherExtension().run()
