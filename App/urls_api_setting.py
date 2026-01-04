from rest_framework.routers import DefaultRouter
from App.api.dropdown_crud_router import DropdownGroupViewSet, DropdownMasterViewSet
from App.api.setting_api import SettingListCreateAPI, SettingDetailAPI
from django.urls import path

router = DefaultRouter()
router.register(r'dropdowns/groups', DropdownGroupViewSet, basename='dropdown-group')
router.register(r'dropdowns/masters', DropdownMasterViewSet, basename='dropdown-master')

urlpatterns = [
    path('settings/', SettingListCreateAPI.as_view(), name='setting-list-create'),
    path('settings/<int:setting_id>/', SettingDetailAPI.as_view(), name='setting-detail'),
]

urlpatterns += router.urls
