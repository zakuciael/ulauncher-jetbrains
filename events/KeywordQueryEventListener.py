""" Contains class for handling keyword events from Ulauncher"""
from __future__ import annotations

import os
import re
from typing import cast

from typing_extensions import TYPE_CHECKING
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

from data.IdeKey import IdeKey
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

        if ide_key is not None:
            projects.extend(extension.get_recent_projects(ide_key))
        else:
            for key in extension.ides:
                projects.extend(extension.get_recent_projects(cast(IdeKey, key)))

        results = []

        if len(projects) == 0:
            results.append(
                ExtensionResultItem(
                    icon=extension.get_ide_icon(
                        ide_key) if ide_key is not None else extension.get_base_icon(),
                    name="No projects found",
                    on_enter=HideWindowAction()
                )
            )
            return RenderResultListAction(results)

        for project in projects:
            results.append(
                ExtensionResultItem(
                    icon=project.icon if project.icon is not None else
                    extension.get_ide_icon(project.ide),
                    name=project.name,
                    description=project.path,
                    on_enter=RunScriptAction(
                        extension.get_ide_launcher_script(project.ide) +
                        f' "{os.path.expanduser(project.path)}" &'
                    ),
                    on_alt_enter=CopyToClipboardAction(project.path)
                )
            )

        return RenderResultListAction(results)
