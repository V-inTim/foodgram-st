from rest_framework import serializers

from foodgram.fields import Base64ImageField
from recipes.serializers import ShortRecipeSerializer
from .models import User, Subscribe


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'password', 'username',
                  "first_name", "last_name", "id", "is_subscribed"]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return Subscribe.objects.filter(
            user=request.user,
            followed_user=obj
        ).exists()
    
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


class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )

    class Meta:
        model = Subscribe
        fields = ['user', 'followed_user']

    def to_representation(self, instance):
        request = self.context.get('request')

        recipes_limit = int(request.query_params.get('recipes_limit', 5))

        user_data = UserSerializer(
            instance.followed_user,
            context={'request': request},
        ).data

        recipes = instance.followed_user.recipes.all()[:recipes_limit]
        recipes_data = ShortRecipeSerializer(recipes, many=True).data

        user_data.update({
            "recipes": recipes_data,
            "recipes_count": instance.followed_user.recipes.count()
        })

        return user_data

    def delete(self):
        user = self.context['request'].user
        followed_user_id = self.initial_data.get('followed_user')
        if not followed_user_id:
            return False
        obj = Subscribe.objects.filter(
            user=user,
            followed_user=followed_user_id,
        ).first()
        if obj:
            obj.delete()
            return True
        return False

    def get_subscriptions(self):
        user = self.context['request'].user
        subscriptions = Subscribe.objects.filter(user=user)
        return [self.to_representation(subscription)
                for subscription in subscriptions]
