from rest_framework import serializers
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
        ]


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]


class PasswordResetRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = [
            'email',
        ]


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField()

    def create(self, validated_data):
        user = self.context['request'].user
        user.set_password(validated_data['new_password'])
        user.save()

        return user
