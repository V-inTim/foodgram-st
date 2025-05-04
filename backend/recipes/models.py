from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from ingredients.models import Ingredient


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(null=False, max_length=200)
    image = models.ImageField(null=False)
    text = models.TextField(null=False)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
    )
    cooking_time = models.PositiveIntegerField(null=False)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField()

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} - {self.amount}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='user_shopping_list'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_shopping_list'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_list'
            )
        ]
        default_related_name = "shopping_list"

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='user_favorite'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_favorite'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]
        default_related_name = "favorites"

    def __str__(self):
        return f'{self.user} - {self.recipe}'
