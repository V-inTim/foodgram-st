from django.contrib import admin
from django.db.models import Count

from .models import Ingredient


class HasRecipesFilter(admin.SimpleListFilter):
    title = 'Наличие в рецептах'
    parameter_name = 'has_recipes'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Есть в рецептах'),
            ('no', 'Нет в рецептах'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(_recipe_count__gt=0)
        if self.value() == 'no':
            return queryset.filter(_recipe_count=0)
        return queryset


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'recipe_count')
    search_fields = ('name',)
    list_filter = ('measurement_unit', HasRecipesFilter)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _recipe_count=Count('ingredient_links', distinct=True)
        )
        return queryset

    @admin.display(description='Количество рецептов', ordering='_recipe_count')
    def recipe_count(self, ingredient):
        return ingredient._recipe_count
