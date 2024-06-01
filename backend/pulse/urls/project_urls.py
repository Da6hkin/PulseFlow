from django.urls import path

from pulse.views.project import ProjectDetailView, ProjectCreateView, ProjectListView, ProjectDetailViewByJWT, \
    ProjectDetailViewFinance

urlpatterns = [
    path('/search', ProjectListView.as_view()),
    path('/<int:pk>', ProjectDetailView.as_view(), name="project-actions-by-pk"),
    path('', ProjectCreateView.as_view()),
    path('/is_pm/<int:project_id>', ProjectDetailViewByJWT.as_view()),
    path('/finance/<int:project_id>', ProjectDetailViewFinance.as_view())
]
