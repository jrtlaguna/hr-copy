from django.conf.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from users.api.v1 import viewsets

router = DefaultRouter()
router.register(r"", viewsets.UserViewSet, basename="users")


urlpatterns = [
    path(r"", include(router.urls)),
]
