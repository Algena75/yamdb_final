import re

from rest_framework import serializers

from users.models import User


class ValidateUserSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        if not re.match(r'[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                f'{value} содержит запрещённые символы.'
            )
        if len(value) > 150:
            raise serializers.ValidationError(
                'Имя пользователя не может быть больше 150 символов.'
            )
        return value


class UserSerializer(ValidateUserSerializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.CharField(required=True, max_length=254)
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        ordering = ['-pk']

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Имя пользователя Me не разрешено"
            )
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                "Имя пользователя содержит запрещенные символы"
            )
        if len(value) > 150:
            raise serializers.ValidationError(
                'Имя пользователя не может содержать более 150 символов'
            )
        return value


class AdminUserSerializer(ValidateUserSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        ordering = ['-pk']


class SignupSerializer(ValidateUserSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')
        ordering = ['-pk']


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
