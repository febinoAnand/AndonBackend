from rest_framework import serializers
from .models import Inbox, Settings, SearchParameter

class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        fields = '__all__'

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'

class SearchParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchParameter
        fields = '__all__'