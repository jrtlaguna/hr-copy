from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import EmployeeFilter
from employees.models import (
    Education,
    Employee,
    EmergencyContact,
    WorkHistory,
)
from employees.api.serializers import (
    EducationSerializer,
    EmployeeSerializer,
    EmergencyContactSerializer,
    WorkHistorySerializer,
)


class EmployeeAPIViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    filter_class = EmployeeFilter
    filter_backends = (filters.DjangoFilterBackend,)
