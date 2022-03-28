""" Contains class for handling keyword events from Ulauncher"""
from __future__ import annotations

import os
import re
from typing import cast, List

from typing_extensions import TYPE_CHECKING
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

from data.IdeKey import IdeKey
from data.IdeProject import IdeProject
from utils.ProjectsList import ProjectsList

if TYPE_CHECKING:
    from main import JetbrainsLauncherExtension


# pylint: disable=too-few-public-methods
class KeywordQueryEventListener(EventListener):
    """ Handles users input and searches for results """

    def on_event(self, event: KeywordQueryEvent, extension: 'JetbrainsLauncherExtension') -> \
            RenderResultListAction:
        """
        Handles the keyword event
        :param event: Event data
        :param extension: Extension class
        :return: List of actions to render
        """

        args = [arg.lower() for arg in re.split("[ /]+", (event.get_argument() or ""))]
        keyword = args[0] if len(args) > 0 else ""
        ide_key: IdeKey | None = None

        if extension.check_ide_key(keyword):
            ide_key = cast(IdeKey, keyword)
        elif keyword in extension.aliases:
            ide_key = extension.aliases.get(keyword)

        query = " ".join(args[1:] if ide_key is not None else args).strip()
        projects = ProjectsList(query, min_score=(60 if len(query) > 0 else 0), limit=8)

        try:
            if ide_key is not None:
                if not extension.get_ide_launcher_script(ide_key):
                    return self.make_error(
                        extension=extension,
                        title="IDE launcher not found",
                        desc="Please verify that you have the IDE installed.",
                        ide_key=ide_key
                    )

                projects.extend(extension.get_recent_projects(ide_key))
            else:
                for key in [key for key in extension.ides if
                            extension.get_ide_launcher_script(key)]:
                    projects.extend(extension.get_recent_projects(cast(IdeKey, key)))
        except FileNotFoundError:
            return self.make_error(
                extension=extension,
                title="Unable to find IDE configuration",
                desc="Make sure that you provided a valid path to the IDE config directory.",
                ide_key=ide_key
            )

        results = []

        if len(projects) == 0:
            return self.make_error(
                extension=extension,
                title="No projects found",
                ide_key=ide_key
            )

        sort_by = extension.preferences.get("sort_by")
        for project in self.sort_projects(list(projects), sort_by):
            results.append(
                ExtensionResultItem(
                    icon=project.icon if project.icon is not None else
                    extension.get_ide_icon(project.ide),
                    name=project.name,
                    description=project.path,
                    on_enter=RunScriptAction(
                        cast(str, extension.get_ide_launcher_script(project.ide)) +
                        f' "{os.path.expanduser(project.path)}" &'
                    ),
                    on_alt_enter=CopyToClipboardAction(project.path)
                )
            )

        return RenderResultListAction(results)

    @staticmethod
    def sort_projects(projects: List[IdeProject], sort_by: str) -> List[IdeProject]:
        """
        Sorts list of projects by a given sorting mode
        :param projects: List of projects to sort
        :param sort_by: Sorting mode
        :return List[IdeProject] Sorted projects
        """

        if sort_by == "recent":
            return sorted(
                projects,
                key=lambda item: -item.timestamp if item.timestamp is not None else 0
            )

        if sort_by in ("ascending", "descending"):
            return sorted(
                projects,
                key=lambda item: item.name,
                reverse=sort_by == "descending"
            )

        return list(projects)

    @staticmethod
    def make_error(extension: 'JetbrainsLauncherExtension', title: str,
                   desc: str | None = None, ide_key: IdeKey | None = None):
        """
        Create an error in form of ExtensionResultItem
        :param extension: Extension class
        :param title: The title of the error
        :param desc: The description of the error
        :param ide_key: The IDE key
        :return RenderResultListAction with the error inside
        """

        return RenderResultListAction([
            ExtensionResultItem(
                icon=extension.get_ide_icon(ide_key) \
                    if ide_key is not None else extension.get_base_icon(),
                name=title,
                description=desc,
                on_enter=HideWindowAction()
            )
        ])
