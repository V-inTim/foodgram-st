from django.contrib import admin
from .models import Recipe, RecipeIngredient, Favorite, ShoppingList
from django.db.models import Count

admin.site.register(RecipeIngredient)
admin.site.register(Favorite)
admin.site.register(ShoppingList)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'cooking_time', 'favorites_count',
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

    def favorites_count(self, obj):
        return obj.favorites_count
    favorites_count.short_description = 'В избранном'
    favorites_count.admin_order_field = 'favorites_count'

    def ingredients_list(self, obj):
        return ", ".join([ing.name for ing in obj.ingredients.all()])
    ingredients_list.short_description = 'Ингредиенты'
