from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=16, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    is_project_manager = models.BooleanField(default=False)


class Company(models.Model):
    name = models.CharField(max_length=100)
    website_link = models.URLField(max_length=200)
    linkedIn_link = models.URLField(max_length=200)
    COMPANY_TYPES = (
        ('IT', 'Information Technology'),
        ('Finance', 'Finance'),
        ('Healthcare', 'Healthcare'),
        ('Retail', 'Retail'),
        ('Manufacturing', 'Manufacturing'),
    )
    company_type = models.CharField(max_length=100, choices=COMPANY_TYPES)


class Worker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    ROLE_TYPES = (
        ('BACK', 'Backend Developer')
    )
    role = models.CharField(max_length=100, choices=ROLE_TYPES)


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True)
    income = models.FloatField(null=True)


class ProjectManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class TaskPriority(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Task(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    priority = models.ForeignKey(TaskPriority, on_delete=models.PROTECT)
    description = models.TextField(max_length=1000, null=True)
    planned_start_date = models.DateField()
    planned_end_date = models.DateField()
    actual_start_date = models.DateField(null=True)
    actual_end_date = models.DateField(null=True)
