from .views import ClientViewSet

from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')


urlpatterns = [
    path('', include(router.urls)),
]
