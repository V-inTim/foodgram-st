from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ingredients.views import IngredientViewSet


router = DefaultRouter()
router.register("ingredients", IngredientViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', include('users.urls')),
    path('recipes/', include('recipes.urls')),
    path('', include(router.urls)),
]
