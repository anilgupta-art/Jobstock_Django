from rest_framework import serializers
from .models import Setting

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['id', 'key', 'value','ResponseBody','client', 'description', 'created_at', 'updated_at']
