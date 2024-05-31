from rest_framework import serializers

from pulse.models import Project
from pulse.serializers.company_serializer import CompanyDetailSerializer


class ProjectCreateSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)

    class Meta:
        model = Project
        fields = ("company", "name", "description", "start_date", "end_date", "income",)


class ProjectUpdateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)
    income = serializers.FloatField(required=False)

    class Meta:
        model = Project
        fields = ("description", "start_date", "end_date", "income",)


class ProjectListSerializer(serializers.ModelSerializer):
    company = CompanyDetailSerializer(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"


class ProjectDetailSerializer(serializers.ModelSerializer):
    company = CompanyDetailSerializer(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
