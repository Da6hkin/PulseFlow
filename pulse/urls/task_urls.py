from django.urls import path

from pulse.views.task import TaskListView, TaskDetailView, TaskCreateView

urlpatterns = [
    path('/search', TaskListView.as_view()),
    path('/<int:pk>', TaskDetailView.as_view(), name="task-actions-by-pk"),
    path('', TaskCreateView.as_view()),
]
