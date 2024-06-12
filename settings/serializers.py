from rest_framework import serializers
from settings.models import Setting

class SettingSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Setting
        fields = ['id', 'logo_path', 'logo_url']

    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo_path and hasattr(obj.logo_path, 'url'):
            return request.build_absolute_uri(obj.logo_path.url)
        return None
