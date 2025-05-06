from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Subscription
from users.serializers import UserSerializer
from recipes.serializers import ShortRecipeSerializer


class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        write_only=True
    )

    class Meta:
        model = Subscription
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
        obj = Subscription.objects.filter(
            user=user,
            followed_user=followed_user_id,
        ).first()
        if obj:
            obj.delete()
            return True
        return False

    def get_subscriptions(self):
        user = self.context['request'].user
        subscriptions = Subscription.objects.filter(user=user)
        return [self.to_representation(subscription)
                for subscription in subscriptions]
