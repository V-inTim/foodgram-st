import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers


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
