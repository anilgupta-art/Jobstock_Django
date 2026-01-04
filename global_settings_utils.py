from App.settings.services import SettingService

def get_setting_value(client, key):
    """
    Returns a dict with 'key' and 'value' for the given client and key from global settings cache.
    Returns None if not found.
    """
    return SettingService.get_setting_value_by_client_and_key(client, key)
