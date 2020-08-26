from django.conf.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from leaves.api.v1 import viewsets

router = DefaultRouter()
router.register(
    r"allocations", viewsets.LeaveAllocationViewSet, basename="leave-allocations"
)
router.register(r"types", viewsets.LeaveTypeViewSet, basename="leave-types")
router.register(
    r"applications", viewsets.LeaveApplicationViewSet, basename="leave-applications"
)
router.register(r"holidays", viewsets.HolidayViewSet, basename="holidays")
router.register(r"holiday-types", viewsets.HolidayTypeViewSet, basename="holiday-types")


urlpatterns = [
    path(r"", include(router.urls)),
]
