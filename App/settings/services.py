from .repositories import SettingRepository
from .schemas import SettingSerializer
from django.core.cache import cache

class SettingService:
    @staticmethod
    def get_setting_value_by_client_and_key(client, key):
            """
            Returns the value for a given client and key from the cached settings list.
            Returns a dict with 'key' and 'value' if found, else None.
            """
            settings_list = SettingService.list_settings_global()
            for item in settings_list:
                # Assumes each item is a dict with 'client', 'key', and 'value' fields
                if item.get('client') == client and item.get('key') == key:
                    return item
                    #return {'key': item.get('key'), 'value': item.get('value')}
            return None
    @staticmethod
    def list_settings():
        settings = SettingRepository.get_all()
        data= SettingSerializer(settings, many=True).data
        return data

    @staticmethod
    def list_settings_global():
        """
        Returns settings as a global cached list, avoiding repeated DB hits.
        Cached for 1 hour (3600 seconds).
        """
        cache_key = 'global_settings_list'
        settings_list = cache.get(cache_key)
        if settings_list is None:
            settings = SettingRepository.get_all()
            settings_list = SettingSerializer(settings, many=True).data
            cache.set(cache_key, settings_list, 3600)
        return settings_list

    @staticmethod
    def get_setting(setting_id):
        setting = SettingRepository.get_by_id(setting_id)
        if not setting:
            return None
        return SettingSerializer(setting).data

    @staticmethod
    def create_setting(data):
        serializer = SettingSerializer(data=data)
        if serializer.is_valid():
            setting = SettingRepository.create(serializer.validated_data)
            return SettingSerializer(setting).data
        return serializer.errors

    @staticmethod
    def update_setting(setting_key, data):
        setting = SettingRepository.get_by_key(setting_key)
        if not setting:
            return None
        # Only update the ResponseBody field
        #update_data = {'ResponseBody': data.get('ResponseBody')}
        update_data = {'ResponseBody': data}
        serializer = SettingSerializer(setting, data=update_data, partial=True)
        if serializer.is_valid():
            SettingRepository.update(setting, serializer.validated_data)
            return SettingSerializer(setting).data
        return serializer.errors

    @staticmethod
    def delete_setting(setting_id):
        setting = SettingRepository.get_by_id(setting_id)
        if not setting:
            return False
        SettingRepository.delete(setting)
        return True
