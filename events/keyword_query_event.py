import re
from typing import cast

from typing_extensions import TYPE_CHECKING
from ulauncher.api.client.EventListener import EventListener

if TYPE_CHECKING:
    from ulauncher.api.shared.event import KeywordQueryEvent
    from main import JetbrainsLauncherExtension
    from types.ide_types import IdeKey


class KeywordQueryEventListener(EventListener):

    def on_event(self, event: 'KeywordQueryEvent', extension: 'JetbrainsLauncherExtension'):
        """
        Handles the keyword event
        :param event: Event object
        :param extension: Extension object
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
