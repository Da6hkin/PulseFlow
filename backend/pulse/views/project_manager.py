from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pulse.auth.authentication import JWTAuthentication
from pulse.filters.project_manager_filter import ProjectManagerFilter
from pulse.models import ProjectManager, Employee, Project
from pulse.permissions import CanInteractProjectManager
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
        try:
            project = project_manager.validated_data["project"]
            existing_project = Project.objects.get(id=project.id)
            if project.company.creator == request.user:
                project_manager.save()
                return Response(project_manager.data, status=status.HTTP_201_CREATED)
            employee = Employee.objects.get(user_id=request.user.id, company=existing_project.company)
            if employee.is_admin:
                project_manager.save()
                return Response(project_manager.data, status=status.HTTP_201_CREATED)
            user_pm = ProjectManager.objects.get(employee=employee)
            if user_pm:
                project_manager.save()
                return Response(project_manager.data, status=status.HTTP_201_CREATED)
            raise Http404("You are not allowed to perform this request")
        except Project.DoesNotExist:
            raise Http404("Project does not exist")
        except (Employee.DoesNotExist, ProjectManager.DoesNotExist):
            raise Http404("You are not allowed to perform this request")


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
    permission_classes = [IsAuthenticated, CanInteractProjectManager]

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
        user = self.request.user
        project_id = self.request.query_params.get('project', None)
        if project_id:
            try:
                project = Project.objects.get(project_id=project_id)
                Employee.objects.get(user_id=user.id, company_id=project.company)
                pms = ProjectManager.objects.all()
                return pms
            except Project.DoesNotExist:
                raise Http404("Project does not exist")
            except Employee.DoesNotExist:
                raise Http404("You do not have permission to perform this action.")
        else:
            raise Http404("You can't perform search without company parameter.")
