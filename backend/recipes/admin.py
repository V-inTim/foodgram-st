from django.contrib import admin
from .models import Recipe, RecipeIngredient, Favorite, ShoppingCard
from django.db.models import Count


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingCard)
class ShoppingCardAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'cooking_time', 'favorites_count',
                    'ingredients_list')
    search_fields = ('name', 'author__username', 'author__email',
                     'ingredients__name')
    list_filter = ('author', 'cooking_time')

    fieldsets = (
        (None, {
            'fields': ('author', 'name', 'image', 'text', 'cooking_time')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            favorites_count=Count('recipe_favorite'),
            ingredients_count=Count('ingredients')
        )

    @admin.display(
        description='В избранном',
        ordering='favorites_count'
    )
    def favorites_count(self, obj):
        return obj.favorites_count

    @admin.display(description='Ингредиенты')
    def ingredients_list(self, obj):
        return ", ".join([ing.name for ing in obj.ingredients.all()])
