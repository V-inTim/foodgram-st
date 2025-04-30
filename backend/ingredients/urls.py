from django.urls import path, include
from .views import IngredientView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', IngredientView)

urlpatterns = [
    path('', include(router.urls)),
]
