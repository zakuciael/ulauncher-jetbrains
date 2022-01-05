""" Contains class for handling keyword events from Ulauncher"""

import re
from typing import cast

from typing_extensions import TYPE_CHECKING
from ulauncher.api.client.EventListener import EventListener

if TYPE_CHECKING:
    from ulauncher.api.shared.event import KeywordQueryEvent
    from main import JetbrainsLauncherExtension


# pylint: disable=too-few-public-methods
class KeywordQueryEventListener(EventListener):
    """ Handles users input and searches for results """

    def on_event(self, event: 'KeywordQueryEvent', extension: 'JetbrainsLauncherExtension'):
        """
        Handles the keyword event
        :param event: Event data
        :param extension: Extension class
        """

        args = [arg.lower() for arg in re.split("[ /]+", (event.get_argument() or ""))]
        keyword = args[0] if len(args) > 0 else ""
        ide_key: 'IdeKey | None' = None

        if extension.check_ide_key(keyword):
            ide_key = cast('IdeKey', keyword)
        elif keyword in extension.aliases:
            ide_key = extension.aliases.get(keyword)

        query = " ".join(args[1:] if ide_key is not None else args).strip()

        extension.handle_query(event, query, ide_key)
