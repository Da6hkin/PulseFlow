from django.urls import path

from pulse.views.project import ProjectDetailView, ProjectCreateView, ProjectListView

urlpatterns = [
    path('/search', ProjectListView.as_view()),
    path('/<int:pk>', ProjectDetailView.as_view(), name="project-actions-by-pk"),
    path('', ProjectCreateView.as_view()),
]
