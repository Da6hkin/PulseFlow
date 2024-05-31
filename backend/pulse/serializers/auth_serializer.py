from rest_framework import serializers


class ObtainTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class CustomTokenDetailSerializer(serializers.Serializer):
    token = serializers.CharField()
