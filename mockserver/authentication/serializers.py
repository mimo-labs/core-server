from rest_framework import serializers
from authentication.models import User


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]
