# from App.repositories.setting_repository import SettingRepository
# from App.schemas.setting_schema import SettingSerializer

# class SettingService:
#     @staticmethod
#     def list_settings():
#         settings = SettingRepository.get_all()
#         return SettingSerializer(settings, many=True).data

#     @staticmethod
#     def get_setting(setting_id):
#         setting = SettingRepository.get_by_id(setting_id)
#         if not setting:
#             return None
#         return SettingSerializer(setting).data

#     @staticmethod
#     def create_setting(data):
#         serializer = SettingSerializer(data=data)
#         if serializer.is_valid():
#             setting = SettingRepository.create(serializer.validated_data)
#             return SettingSerializer(setting).data
#         return serializer.errors

#     @staticmethod
#     def update_setting(setting_id, data):
#         setting = SettingRepository.get_by_id(setting_id)
#         if not setting:
#             return None
#         serializer = SettingSerializer(setting, data=data, partial=True)
#         if serializer.is_valid():
#             SettingRepository.update(setting, serializer.validated_data)
#             return SettingSerializer(setting).data
#         return serializer.errors

#     @staticmethod
#     def delete_setting(setting_id):
#         setting = SettingRepository.get_by_id(setting_id)
#         if not setting:
#             return False
#         SettingRepository.delete(setting)
#         return True
