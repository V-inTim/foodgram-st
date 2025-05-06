from django.urls import path, include
from .views import IngredientViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
