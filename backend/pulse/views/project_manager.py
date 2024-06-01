from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pulse.auth.authentication import JWTAuthentication
from pulse.filters.project_manager_filter import ProjectManagerFilter
from pulse.models import ProjectManager
from pulse.serializers.error_serializer import DummyDetailSerializer, DummyDetailAndStatusSerializer
from pulse.serializers.project_manager_serializer import ProjectManagerCreateSerializer, ProjectManagerDetailSerializer, \
    ProjectManagerListSerializer


@extend_schema(tags=["Project Manager"])
@extend_schema_view(
    post=extend_schema(
        summary="Create project manager",
        request=ProjectManagerCreateSerializer,
        responses={
            status.HTTP_200_OK: ProjectManagerDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
)
class ProjectManagerCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        project_manager = ProjectManagerCreateSerializer(data=request.data)
        project_manager.is_valid(raise_exception=True)
        project_manager.save()
        return Response(project_manager.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Project Manager"])
@extend_schema_view(
    get=extend_schema(
        summary="Detailed info about project manager",
        responses={
            status.HTTP_200_OK: ProjectManagerDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    delete=extend_schema(
        summary="Disable project manager",
        responses={
            status.HTTP_200_OK: DummyDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    )
)
class ProjectManagerDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_project_manager(self, pk):
        try:
            return ProjectManager.objects.get(pk=pk)
        except ProjectManager.DoesNotExist:
            raise Http404("ProjectManager does not exist")

    def get(self, request, pk):
        project_manager = self.get_project_manager(pk)
        serializer = ProjectManagerDetailSerializer(project_manager)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        project_manager = self.get_project_manager(pk)
        project_manager.disabled = True
        project_manager.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Project Manager"])
@extend_schema_view(
    get=extend_schema(
        summary="Search project managers",
        responses={
            status.HTTP_200_OK: ProjectManagerListSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        }
    )
)
class ProjectManagerListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ProjectManager.objects.all()
    serializer_class = ProjectManagerListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProjectManagerFilter

    def get_queryset(self):
        projects = ProjectManager.objects.all()
        return projects



