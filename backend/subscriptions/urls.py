from django.urls import path
from .views import SubscriptionDetailAPIView, SubscriptionListAPIView


urlpatterns = [
    path(
        '<int:pk>/subscribe/',
        SubscriptionDetailAPIView.as_view(),
        name='subscribe',
    ),
    path(
        'subscriptions/',
        SubscriptionListAPIView.as_view(),
        name='subscription-list',
    ),
]
