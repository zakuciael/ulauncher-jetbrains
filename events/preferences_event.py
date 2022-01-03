from typing_extensions import TYPE_CHECKING
from ulauncher.api.client.EventListener import EventListener

if TYPE_CHECKING:
    from ulauncher.api.shared.event import PreferencesEvent
    from main import JetbrainsLauncherExtension


class PreferencesEventListener(EventListener):
    def on_event(self, event: 'PreferencesEvent', extension: 'JetbrainsLauncherExtension'):
        """
        Sets preferences on the initial run of the extension and updates the aliases list
        :param event: Event containing all preferences
        :param extension: The extension to update
        """

        extension.preferences.update(event.preferences)
        extension.parse_aliases(event.preferences.get("custom_aliases"))
