from drf_writable_nested.mixins import UniqueFieldsMixin
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        email = validated_data.get("email")
        validated_data["username"] = email.split("@")[0]
        return super().create(validated_data)
