from django.conf.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from leaves.api.v1 import viewsets

router = DefaultRouter()
router.register(r"types", viewsets.LeaveTypeViewSet, basename="leave-types")


urlpatterns = [
    path(r"", include(router.urls)),
]
