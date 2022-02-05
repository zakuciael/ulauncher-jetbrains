""" Contains class for handling initial preference event from Ulauncher"""

from typing_extensions import TYPE_CHECKING
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import PreferencesEvent

if TYPE_CHECKING:
    from main import JetbrainsLauncherExtension


# pylint: disable=too-few-public-methods
class PreferencesEventListener(EventListener):
    """ Handles initial user settings and parses them """

    def on_event(self, event: PreferencesEvent, extension: 'JetbrainsLauncherExtension') -> None:
        """
        Handles the preference event
        :param event: Event data
        :param extension: Extension class
        """

        if "studio_config_path" not in event.preferences:
            event.preferences["studio_config_path"] = "~/.config/Google"

        extension.preferences.update(event.preferences)
        extension.parse_aliases(event.preferences.get("custom_aliases"))
