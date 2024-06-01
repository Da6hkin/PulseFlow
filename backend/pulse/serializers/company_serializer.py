from rest_framework import serializers

from pulse.models import Company


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class CompanyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class CompanyUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    website = serializers.URLField(required=False)

    class Meta:
        model = Company
        fields = ("name", "website",)
