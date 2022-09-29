from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import SubscriptionsViewSet

router = DefaultRouter()
router.register('users', SubscriptionsViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
