from rest_framework import serializers

from pulse.models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class UserDetailSerializer(serializers.ModelSerializer):
    # category = serializers.SlugRelatedField(slug_field="name",read_only=True)
    # slug_field = field in another table
    class Meta:
        model = User
        exclude = ("password",)


class UserCreateSerializer(serializers.ModelSerializer):
    disabled = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = ("name", "surname", "password", "email", "disabled")


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)
    disabled = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ("password", "disabled")
