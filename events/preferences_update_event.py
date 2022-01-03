from typing_extensions import TYPE_CHECKING
from ulauncher.api.client.EventListener import EventListener

if TYPE_CHECKING:
    from ulauncher.api.shared.event import PreferencesUpdateEvent
    from main import JetbrainsLauncherExtension


class PreferencesUpdateEventListener(EventListener):
    def on_event(self, event: 'PreferencesUpdateEvent', extension: 'JetbrainsLauncherExtension'):
        """
        Updates preferences with the new value and parses aliases if needed
        :param event: Event containing new values for a specific preference
        :param extension: The extension to update
        """
        extension.preferences[event.id] = event.new_value

        if event.id == "custom_aliases":
            extension.parse_aliases(event.new_value)
