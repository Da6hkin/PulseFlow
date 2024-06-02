from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pulse.auth.authentication import JWTAuthentication
from pulse.filters.task_filter import TaskFilter
from pulse.models import Task, Project, Employee, ProjectManager
from pulse.permissions import CanInteractTask
from pulse.serializers.error_serializer import DummyDetailSerializer, DummyDetailAndStatusSerializer
from pulse.serializers.task_serializer import TaskCreateSerializer, TaskDetailSerializer, TaskUpdateSerializer, \
    TaskListSerializer


@extend_schema(tags=["Task"])
@extend_schema_view(
    post=extend_schema(
        summary="Create task",
        request=TaskCreateSerializer,
        responses={
            status.HTTP_200_OK: TaskDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
)
class TaskCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        task = TaskCreateSerializer(data=request.data)
        task.is_valid(raise_exception=True)
        try:
            project = task.validated_data["project"]
            if request.user == project.company.creator:
                task.save()
                return Response(task.data, status=status.HTTP_201_CREATED)
            employee = Employee.objects.get(user_id=request.user.id, company=project.company)
            if employee.is_project_manager:
                task.save()
                return Response(task.data, status=status.HTTP_201_CREATED)
            user_pm = ProjectManager.objects.get(employee=employee)
            if user_pm:
                task.save()
                return Response(task.data, status=status.HTTP_201_CREATED)
            else:
                raise Http404("You are not allowed to perform this request")
        except Project.DoesNotExist:
            raise Http404("Project does not exist")
        except (Employee.DoesNotExist, ProjectManager.DoesNotExist):
            raise Http404("You are not allowed to perform this request")


@extend_schema(tags=["Task"])
@extend_schema_view(
    get=extend_schema(
        summary="Detailed info about task",
        responses={
            status.HTTP_200_OK: TaskDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    put=extend_schema(
        summary="Update task",
        request=TaskUpdateSerializer,
        responses={
            status.HTTP_200_OK: TaskDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    ),
    delete=extend_schema(
        summary="Delete task",
        responses={
            status.HTTP_200_OK: DummyDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    )
)
class TaskDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CanInteractTask]

    def get_task(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404("Project does not exist")

    def get(self, request, pk):
        task = self.get_task(pk)
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = self.get_task(pk)
        serializer = TaskUpdateSerializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        updated_task = TaskDetailSerializer(task)
        return Response(updated_task.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        task = self.get_task(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Task"])
@extend_schema_view(
    get=extend_schema(
        summary="Search tasks",
        responses={
            status.HTTP_200_OK: TaskListSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        }
    )
)
class TaskListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        user = self.request.user
        project = self.request.query_params.get('project', None)
        if project:
            try:
                project = Project.objects.get(id=project)
                Employee.objects.get(user_id=user.id, company=project.company)
                tasks = Task.objects.all()
                return tasks
            except Project.DoesNotExist:
                raise Http404("Project does not exist")
            except Employee.DoesNotExist:
                raise Http404("You do not have permission to perform this action.")
        else:
            raise Http404("You can't perform search without project parameter.")
