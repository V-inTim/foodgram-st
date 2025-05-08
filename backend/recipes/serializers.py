from collections import defaultdict

from rest_framework import serializers

from .models import (
    Recipe,
    RecipeIngredient,
    ShoppingCard,
    Favorite,
)
from api.fields import Base64ImageField
from users.serializers import UserSerializer


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True,
    )
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'measurement_unit', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        required=True,
        source='recipe_ingredients',
    )

    class Meta:
        model = Recipe
        fields = ['id', 'author', 'name', 'image',
                  'text', 'ingredients', 'cooking_time']

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if 'image' not in data or data['image'] is None:
                raise serializers.ValidationError(
                    {"image": "Это поле обязательно при создании рецепта"}
                )
        return data

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient_data['ingredient']['id'],
                amount=ingredient_data['amount'],
            )

        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        instance = super().update(instance, validated_data)

        instance.ingredients.clear()
        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=instance,
                ingredient_id=ingredient_data['ingredient']['id'],
                amount=ingredient_data['amount']
            )

        return instance


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCard
        fields = ['recipe', 'user']

    def to_representation(self, instance):
        return ShortRecipeSerializer(instance.recipe).data

    def delete(self):
        user = self.context['request'].user
        recipe_id = self.initial_data.get('recipe')
        if not recipe_id:
            return False
        obj = ShoppingCard.objects.filter(user=user, recipe=recipe_id).first()
        if obj:
            obj.delete()
            return True
        return False

    def get_shopping_list(self):
        user = self.context['request'].user
        shopping_list = (
            ShoppingCard.objects.filter(user=user)
            .select_related('recipe')
            .prefetch_related('recipe__recipe_ingredients__ingredient')
        )

        ingredient_data = defaultdict(
            lambda: {'name': '', 'measurement_unit': '', 'amount': 0}
        )

        for item in shopping_list:
            recipe = item.recipe
            for ri in recipe.recipe_ingredients.all():
                ingredient = ri.ingredient
                key = ingredient.id
                ingredient_data[key]['name'] = ingredient.name
                ingredient_data[key]['measurement_unit'] = (
                    ingredient.measurement_unit
                )
                ingredient_data[key]['amount'] += ri.amount

        lines = []
        for data in ingredient_data.values():
            name = data['name']
            unit = data['measurement_unit']
            amount = data['amount']
            lines.append(f'{name} ({unit}) — {amount}')

        return '\n'.join(lines)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['recipe', 'user']

    def to_representation(self, instance):
        return ShortRecipeSerializer(instance.recipe).data

    def delete(self):
        user = self.context['request'].user
        recipe_id = self.initial_data.get('recipe')
        if not recipe_id:
            return False
        obj = Favorite.objects.filter(user=user, recipe=recipe_id).first()
        if obj:
            obj.delete()
            return True
        return False
