from django.urls import path
from .api import SettingListCreateAPI, SettingDetailAPI

urlpatterns = [
    path('settings/', SettingListCreateAPI.as_view(), name='setting_list_create_api'),
    path('settings/<int:setting_id>/', SettingDetailAPI.as_view(), name='setting_detail_api'),
]
