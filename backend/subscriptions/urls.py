from django.urls import include, path
from rest_framework.routers import DefaultRouter

from subscriptions.views import SubscriptionViewSet

router = DefaultRouter()
router.register('', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
]
