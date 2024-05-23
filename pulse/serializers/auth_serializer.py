from rest_framework import serializers


class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class CustomTokenDetailSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
