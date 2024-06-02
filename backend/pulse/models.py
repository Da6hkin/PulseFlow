from django.contrib.auth.models import AbstractUser
from django.db import models

STATE = (
    ('todo', 'To Do'),
    ('research', 'Research'),
    ('in_progress', 'In Progress'),
    ('testing', 'Testing'),
    ('done', 'Done'),
)

RATE_TYPES = (
    ('fixed', 'Fixed'),
    ('hour', 'Hour Rate')
)


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=100, null=False)
    surname = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=255, unique=True)
    disabled = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Company(models.Model):
    name = models.CharField(max_length=100)
    unique_identifier = models.CharField(max_length=100, unique=True)
    website = models.URLField(max_length=200, null=True)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    is_project_manager = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'company',)


class Project(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=5000, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    income = models.FloatField()


class ProjectManager(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    disabled = models.BooleanField(default=False)

    class Meta:
        unique_together = ('employee', 'project',)


class Task(models.Model):
    name = models.CharField(max_length=300)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    state = models.CharField(max_length=100, choices=STATE)
    priority = models.IntegerField()
    description = models.CharField(max_length=1000, null=True)
    planned_start_date = models.DateTimeField()
    planned_end_date = models.DateTimeField()
    hours_spent = models.IntegerField(default=0)


class Assigned(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    rate_type = models.CharField(max_length=100, choices=RATE_TYPES, null=True)
    rate = models.FloatField(null=True)


class ChatMessage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=True)
