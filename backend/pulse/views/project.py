from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pulse.auth.authentication import JWTAuthentication
from pulse.filters.project_filter import ProjectFilter
from pulse.models import Project, Employee, ProjectManager, Task, Assigned, RATE_TYPES
from pulse.permissions import CanInteractProject
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

    def check_for_pm(self, employee, project):
        try:
            ProjectManager.objects.get(employee=employee, project=project)
        except ProjectManager.DoesNotExist:
            pm = ProjectManager(employee=employee, project=project, disabled=False)
            pm.save()

    def post(self, request):
        project = ProjectCreateSerializer(data=request.data)
        project.is_valid(raise_exception=True)
        company = project.validated_data["company"]
        try:
            employee = Employee.objects.get(user_id=request.user.id, company=company)
            if employee.is_admin:
                saved_project = project.save()
                self.check_for_pm(employee, saved_project)
                return Response(project.data, status=status.HTTP_201_CREATED)
            pm = ProjectManager.objects.get(employee=employee)
            if pm:
                saved_project = project.save()
                self.check_for_pm(employee, saved_project)
                return Response(project.data, status=status.HTTP_201_CREATED)
            else:
                raise Http404("You are not allowed to perform this request")
        except (Employee.DoesNotExist, ProjectManager.DoesNotExist):
            raise Http404("You are not allowed to perform this request")


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
    permission_classes = [IsAuthenticated, CanInteractProject]

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
        user = self.request.user
        company = self.request.query_params.get('company', None)
        if company:
            try:
                Employee.objects.get(user_id=user.id, company_id=company)
                projects = Project.objects.all()
                return projects
            except Employee.DoesNotExist:
                raise Http404("You do not have permission to perform this action.")
        else:
            raise Http404("You can't perform search without company parameter.")


@extend_schema(tags=["Project"])
@extend_schema_view(
    get=extend_schema(
        summary="Is user a project manager",
        responses={
            status.HTTP_200_OK: ProjectDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    )
)
class ProjectDetailViewByJWT(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_project(self, project_id):
        try:
            return Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise Http404("Project does not exist")

    def get(self, request, project_id):
        project = self.get_project(project_id)
        user_id = request.user.id
        if project.company.creator.id == user_id:
            return Response(True, status=status.HTTP_200_OK)
        try:
            employee = Employee.objects.get(user_id=user_id, company_id=project.company.id)
        except Employee.DoesNotExist:
            raise Http404("User is not employee in this company")
        try:
            project_manager = ProjectManager.objects.get(employee_id=employee.id, project_id=project.id)
            if project_manager:
                return Response(True, status=status.HTTP_200_OK)
        except ProjectManager.DoesNotExist:
            return Response(False, status=status.HTTP_200_OK)


@extend_schema(tags=["Project"])
@extend_schema_view(
    get=extend_schema(
        summary="Project Finances",
        responses={
            status.HTTP_200_OK: ProjectDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
            status.HTTP_404_NOT_FOUND: DummyDetailSerializer
        }
    )
)
class ProjectDetailViewFinance(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_project(self, project_id):
        try:
            return Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise Http404("Project does not exist")

    def get(self, request, project_id):
        project = self.get_project(project_id)
        user_id = request.user.id
        try:
            employee = Employee.objects.get(user_id=user_id, company_id=project.company.id)
        except Employee.DoesNotExist:
            employee = None
        try:
            if employee:
                project_manager = ProjectManager.objects.get(employee_id=employee.id, project_id=project.id)
            else:
                project_manager = None
        except ProjectManager.DoesNotExist:
            project_manager = None
        if project_manager is None and employee is None and project.company.creator != request.user:
            raise Http404("You do not have permission to perform this action.")
        else:
            if employee and employee.is_admin == False:
                raise Http404("You do not have permission to perform this action.")
            else:
                tasks = Task.objects.filter(project_id=project.id, state='done')
                assigned = Assigned.objects.filter(task_id__in=tasks.values('id'))
                assigned_to_return = {}
                all_to_pay = 0
                for assign in assigned:
                    if assign.rate_type:
                        salary = None
                        if assign.rate_type == 'fixed':
                            salary = assign.rate
                        else:
                            if assign.task.hours_spent > 0:
                                salary = assign.rate * assign.task.hours_spent
                        assigned_user = assign.employee.user
                        name = f"{assigned_user.email}"
                        task = assign.task
                        if salary is not None:
                            all_to_pay += salary
                            if name not in assigned_to_return:
                                assigned_to_return[name] = []
                            assigned_to_return[name].append(
                                {"task_id": task.id, "name": task.name, "salary": salary,
                                 "hours_spent": task.hours_spent})
                return_data = {
                    "income": project.income,
                    "tasks": assigned_to_return,
                    "profit": project.income - all_to_pay,
                }
                return Response(return_data, status=status.HTTP_200_OK)
