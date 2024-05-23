from django.contrib.postgres.fields import ArrayField
from django.db import models

STATE = (
    ('todo', 'To Do'),
    ('research', 'Research'),
    ('in_progress', 'In Progress'),
    ('testing', 'testing'),
    ('done', 'done'),
)

RATE_TYPES = (
    ('FIXED', 'Fixed Price'),
    ('HOUR', 'Hour rate')
)


class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    disabled = models.BooleanField(default=False)


class Company(models.Model):
    name = models.CharField(max_length=100)
    unique_identifier = models.CharField(max_length=100, unique=True)
    website = models.URLField(max_length=200, null=True)
    logo = models.BinaryField(null=True)


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    is_project_manager = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True)
    income = models.FloatField(null=True)
    #


class ProjectManager(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    disabled = models.BooleanField(default=False)


class Task(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    state = models.CharField(max_length=100, choices=STATE)
    priority = models.IntegerField()
    description = models.TextField(max_length=1000, null=True)
    planned_start_date = models.DateField()
    planned_end_date = models.DateField()
    actual_start_date = models.DateField(null=True)
    actual_end_date = models.DateField(null=True)


class Assigned(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    rate_type = models.CharField(max_length=100, choices=RATE_TYPES, null=True)
    rate = models.FloatField(null=True)


class ChatMessage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=True)
