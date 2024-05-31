from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pulse.auth.authentication import JWTAuthentication
from pulse.filters.project_filter import ProjectFilter
from pulse.models import Project
from pulse.serializers.error_serializer import DummyDetailSerializer, DummyDetailAndStatusSerializer
from pulse.serializers.project_serializer import ProjectCreateSerializer, ProjectDetailSerializer, \
    ProjectUpdateSerializer, ProjectListSerializer


@extend_schema(tags=["Project"])
@extend_schema_view(
    post=extend_schema(
        summary="Create project",
        request=ProjectCreateSerializer,
        responses={
            status.HTTP_200_OK: ProjectDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
)
class ProjectCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        employee = ProjectCreateSerializer(data=request.data)
        employee.is_valid(raise_exception=True)
        employee.save()
        return Response(employee.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Project"])
@extend_schema_view(
    get=extend_schema(
        summary="Detailed info about project",
        responses={
            status.HTTP_200_OK: ProjectDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    put=extend_schema(
        summary="Update project",
        request=ProjectUpdateSerializer,
        responses={
            status.HTTP_200_OK: ProjectDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    delete=extend_schema(
        summary="Delete project",
        responses={
            status.HTTP_200_OK: DummyDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    )
)
class ProjectDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_project(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404("Project does not exist")

    def get(self, request, pk):
        project = self.get_project(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        project = self.get_project(pk)
        serializer = ProjectUpdateSerializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        updated_project = ProjectDetailSerializer(project)
        return Response(updated_project.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        project = self.get_project(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Project"])
@extend_schema_view(
    get=extend_schema(
        summary="Search projects",
        responses={
            status.HTTP_200_OK: ProjectListSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        }
    )
)
class ProjectListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProjectFilter

    def get_queryset(self):
        projects = Project.objects.all()
        return projects
