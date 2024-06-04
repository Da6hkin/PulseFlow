from django.urls import path

from pulse.views.project_manager import ProjectManagerListView, ProjectManagerDetailView, ProjectManagerCreateView, \
    ProjectManagerDetailViewDelete

urlpatterns = [
    path('/search', ProjectManagerListView.as_view()),
    path('/<int:pk>', ProjectManagerDetailView.as_view(), name="project-manager-actions-by-pk"),
    path('', ProjectManagerCreateView.as_view()),
    path('/delete/<int:pk>', ProjectManagerDetailViewDelete.as_view())
]
