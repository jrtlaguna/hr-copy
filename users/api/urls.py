from django.conf.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from users.api import viewsets

router = DefaultRouter()
router.register(r'', viewsets.EmployeeAPIViewSet, basename="users")


urlpatterns = [
    path(r'', include(router.urls)),
]
