from rest_framework import serializers
from .models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['user_id', 'username']
        extra_kwargs = {
            'username': {'required': False, 'allow_blank': True}
        }