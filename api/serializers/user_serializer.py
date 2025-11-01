from rest_framework import serializers
from api import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = [
            "id",
            "auth0_id",
            "username",
            "email",
            "nickname",
            "role",
            "is_locked",
        ]
