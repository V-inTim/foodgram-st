from django_filters import filters
from django_filters.rest_framework import FilterSet

from .models import Recipe


class RecipeFilter(FilterSet):
    is_favorited = filters.CharFilter(method="filter_is_favorited")
    is_in_shopping_cart = filters.CharFilter(
        method="filter_is_in_shopping_cart"
    )

    def filter_is_favorited(self, queryset, name, value):
        if value in {'1', '0'}:
            value = bool(int(value))
            if value and self.request.user.is_authenticated:
                return queryset.filter(
                    recipe_favorite__user=self.request.user,
                )
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value in {'1', '0'}:
            value = bool(int(value))
            if value and self.request.user.is_authenticated:
                return queryset.filter(
                    recipe_shopping_list__user=self.request.user,
                )
        return queryset

    class Meta:
        model = Recipe
        fields = ("author", "is_favorited", "is_in_shopping_cart")
