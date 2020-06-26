from rest_framework import status, viewsets
from rest_framework.response import Response

from .filters import UserFilter
from users.models import User
from .serializers import UserSerializer


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
