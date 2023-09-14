""" Contains class for handling preference update events from Ulauncher"""

from typing_extensions import TYPE_CHECKING
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import PreferencesUpdateEvent

if TYPE_CHECKING:
    from main import JetbrainsLauncherExtension


# pylint: disable=too-few-public-methods
class PreferencesUpdateEventListener(EventListener):
    """ Handles updates to user settings and parses them """

    def on_event(self, event: PreferencesUpdateEvent, extension: 'JetbrainsLauncherExtension') -> \
            None:
        """
        Handles the preference update event
        :param event: Event data
        :param extension: Extension class
        """

        extension.preferences[event.id] = event.new_value
        if event.id == "custom_aliases":
            extension.set_aliases(extension.parse_aliases(event.new_value))
