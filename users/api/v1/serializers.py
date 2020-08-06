from drf_writable_nested.mixins import UniqueFieldsMixin
from rest_framework import serializers

from users.models import User


class UserSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "is_active",
        ]
