from django.http import Http404
from rest_framework.permissions import BasePermission

from pulse.exceptions import SimplePermissionDenied
from pulse.models import ProjectManager, User, Company, Employee, Project, Task, Assigned


class IsAssociatedWithProject(BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        try:
            project_manager = ProjectManager.objects.get(user_id=user_id, pk=view.kwargs['pk'])
            return project_manager.user == request.user
        except ProjectManager.DoesNotExist:
            raise SimplePermissionDenied()


class IsSameUser(BasePermission):
    def has_permission(self, request, view):
        request_user = request.user
        try:
            user = User.objects.get(pk=view.kwargs['pk'])
            return request_user == user
        except User.DoesNotExist:
            raise Http404("User does not exist")


class IsAssociatedWithCompany(BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        try:
            company = Company.objects.get(pk=view.kwargs['pk'])
            if company.creator == request.user:
                return True
            employee = Employee.objects.get(user_id=user_id, company_id=company.id)
            if employee:
                return True
            else:
                return False
        except Employee.DoesNotExist:
            raise SimplePermissionDenied()
        except ProjectManager.DoesNotExist:
            raise SimplePermissionDenied()


class IsAssociatedWithEmployee(BasePermission):
    def has_permission(self, request, view):
        try:
            employee = Employee.objects.get(pk=view.kwargs['pk'])
            return employee.user == request.user
        except Employee.DoesNotExist:
            raise Http404("Employee does not exist")


class CanInteractProject(BasePermission):
    def has_permission(self, request, view):
        try:
            project = Project.objects.get(pk=view.kwargs['pk'])
            employee = Employee.objects.get(user_id=request.user.id, company=project.company)
            if employee.is_admin:
                return True
            project_manager = ProjectManager.objects.get(project=project, employee=employee)
            if project_manager:
                return True
            else:
                return False
        except Project.DoesNotExist:
            raise Http404("Project does not exist")
        except Employee.DoesNotExist:
            raise SimplePermissionDenied()
        except ProjectManager.DoesNotExist:
            raise SimplePermissionDenied()


class CanInteractProjectManager(BasePermission):
    def has_permission(self, request, view):
        try:
            pm = ProjectManager.objects.get(pk=view.kwargs['pk'])
            employee = Employee.objects.get(user_id=request.user.id, company=pm.project.company)
            if request.user == pm.project.company.creator:
                return True
            if employee.is_admin:
                return True
            project_manager = ProjectManager.objects.get(project=pm.project, employee=employee)
            if project_manager:
                return True
            else:
                return False
        except ProjectManager.DoesNotExist:
            raise Http404("Project Manager does not exist")
        except Employee.DoesNotExist:
            raise SimplePermissionDenied()


class CanInteractTask(BasePermission):
    def has_permission(self, request, view):
        try:
            task = Task.objects.get(pk=view.kwargs['pk'])
            project = Project.objects.get(id=task.project.id)
            employee = Employee.objects.get(user_id=request.user.id, company=project.company)
            if employee:
                return True
            else:
                return False
        except Task.DoesNotExist:
            raise Http404("Task does not exist")
        except Project.DoesNotExist:
            raise SimplePermissionDenied()
        except Employee.DoesNotExist:
            raise SimplePermissionDenied()


class CanInteractAssigned(BasePermission):
    def has_permission(self, request, view):
        try:
            assigned = Assigned.objects.get(pk=view.kwargs['pk'])
            if assigned.employee.user.id == request.user.id:
                return True
            employee = Employee.objects.get(user_id=request.user.id, company_id=assigned.employee.company.id)
            if employee.is_admin:
                return True
            project_manager = ProjectManager.objects.get(project=assigned.task.project, employee=employee)
            if project_manager:
                return True
        except Assigned.DoesNotExist:
            raise Http404("Assigned does not exist")
        except Employee.DoesNotExist:
            raise SimplePermissionDenied()
        except ProjectManager.DoesNotExist:
            raise SimplePermissionDenied()

