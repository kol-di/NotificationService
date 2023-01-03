from .views import MailingViewSet

from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'mailings', MailingViewSet, basename='mailing')


urlpatterns = [
    path('', include(router.urls)),
]
