import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                format, imgstr = data.split(';base64,')
                ext = format.split('/')[1]

                image_data = base64.b64decode(imgstr)

                file_name = f"{uuid.uuid4()}.{ext}"
                return ContentFile(image_data, name=file_name)
            except Exception:
                raise serializers.ValidationError("Невалидная строка Base64")
        else:
            raise serializers.ValidationError(
                "Данные должны быть строкой Base64"
            )


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username',
                  "first_name", "last_name", "id"]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserAvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=True)

    class Meta:
        model = User
        fields = ['avatar']

    def update(self, instance, validated_data):
        avatar = validated_data.get('avatar', None)

        if avatar:
            instance.avatar = avatar
            instance.save()

        return instance

    def delete_avatar(self, user):
        user.avatar = None
        user.save()


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Неверный текущий пароль.")
        return value

    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
