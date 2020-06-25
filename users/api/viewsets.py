from rest_framework import (
    generics,
    status,
    viewsets,
    permissions
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .filters import EmployeeFilter


from users.models import (
    Employee,
    User,
    EmergencyContact,
    WorkHistory,
    Education
)
from users.api.serializers import (
    EmployeeSerializer,
    EmergencyContactSerializer,
    WorkHistorySerializer,
    EducationSerializer,
    )


    

class EmployeeAPIViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    filter_class = EmployeeFilter
    filter_backends = (filters.DjangoFilterBackend,)



    @action(detail=True, url_path='emergency-contacts', methods=['GET'])
    def get_emergency_contacts(self, request, pk):

        queryset = EmergencyContact.objects.filter(employee=pk)   
        serializer = EmergencyContactSerializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, url_path='work-history', methods=['GET'])
    def get_work_history(self, request, pk):

        queryset = WorkHistory.objects.filter(employee=pk)   
        serializer = WorkHistorySerializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, url_path='education', methods=['GET'])
    def get_education(self, request, pk):

        queryset = Education.objects.filter(employee=pk)   
        serializer = EducationSerializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


# class WorkHistoryAPIViewSet(viewsets.ModelViewSet):
#     queryset = WorkHistory.objects.all()
#     serializer_class = WorkHistorySerializer
    

# class EducationAPIViewSet(viewsets.ModelViewSet):
#     queryset = Education.objects.all()
#     serializer_class = EducationSerializer
#     permission_classes = [permissions.AllowAny]


# class EmergencyContactAPIViewSet(viewsets.ModelViewSet):
#     queryset = EmergencyContact.objects.all()
#     serializer_class = EmergencyContactSerializer
    
    