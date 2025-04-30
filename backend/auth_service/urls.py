from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AuthUserView, AvatarUserView, PasswordChangeView


router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('me/', AuthUserView.as_view()),
    path('me/avatar/', AvatarUserView.as_view()),
    path('set_password/', PasswordChangeView.as_view()),
    path('', include(router.urls)),
    
]