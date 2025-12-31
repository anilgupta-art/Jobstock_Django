from App.models import Setting

class SettingRepository:
    @staticmethod
    def get_all():
        return Setting.objects.all()

    @staticmethod
    def get_by_id(setting_id):
        return Setting.objects.filter(id=setting_id).first()

    @staticmethod
    def get_by_key(key):
        return Setting.objects.filter(key=key).first()

    @staticmethod
    def create(data):
        return Setting.objects.create(**data)

    @staticmethod
    def update(setting, data):
        for attr, value in data.items():
            setattr(setting, attr, value)
        setting.save()
        return setting

    @staticmethod
    def delete(setting):
        setting.delete()
