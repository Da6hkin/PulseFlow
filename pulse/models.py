from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    is_project_manager = models.BooleanField(default=False)


class Company(models.Model):
    name = models.CharField(max_length=100)
    unique_identifier = models.CharField(max_length=100, unique=True)
    website_link = models.URLField(max_length=200, null=True)
    COMPANY_TYPES = (
        ('IT', 'Information Technology'),
        ('Finance', 'Finance'),
        ('Healthcare', 'Healthcare'),
        ('Retail', 'Retail'),
        ('Manufacturing', 'Manufacturing'),
    )
    company_type = models.CharField(max_length=100, choices=COMPANY_TYPES)
    logo = models.BinaryField(null=True)


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    ROLE_TYPES = (
        ('CREATOR', 'Company Creator'),
        ('BACK', 'Backend Developer')
    )
    role = models.CharField(max_length=100, choices=ROLE_TYPES)


class TaskState(models.Model):
    name = models.CharField(max_length=100)


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True)
    income = models.FloatField(null=True)
    files = models.CharField(null=True)


class ProjectStates(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    state = models.ForeignKey(TaskState, on_delete=models.PROTECT)


class ProjectManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Task(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    state = models.ForeignKey(TaskState, on_delete=models.PROTECT)
    priority = models.IntegerField()
    description = models.TextField(max_length=1000, null=True)
    planned_start_date = models.DateField()
    planned_end_date = models.DateField()
    actual_start_date = models.DateField(null=True)
    actual_end_date = models.DateField(null=True)


class Assigned(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    RATE_TYPES = (
        ('FIXED', 'Fixed Price'),
        ('HOUR', 'Hour rate')
    )
    rate_type = models.CharField(max_length=100, choices=RATE_TYPES, null=True)
    rate = models.FloatField(null=True)
