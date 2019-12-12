from rest_framework import serializers
from authentication.models import User


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(source='email')

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
