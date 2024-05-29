from rest_framework import serializers

from pulse.models import Project


class ProjectCreateSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)

    class Meta:
        model = Project
        fields = ("name", "description", "start_date", "end_date", "income",)


class ProjectUpdateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)
    income = serializers.FloatField(required=False)

    class Meta:
        model = Project
        fields = ("description", "start_date", "end_date", "income",)


class ProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
