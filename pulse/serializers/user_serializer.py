from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from pulse.models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "surname", "email", "disabled")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "surname", "email", "disabled")


class UserCreateSerializer(serializers.ModelSerializer):
    disabled = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = ("name", "surname", "password", "email", "disabled")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)
    disabled = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ("password", "disabled")
