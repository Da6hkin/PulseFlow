from django.urls import path

from pulse.views.assigned import AssignedListView, AssignedDetailView, AssignedCreateView

urlpatterns = [
    path('/search', AssignedListView.as_view()),
    path('/<int:pk>', AssignedDetailView.as_view(), name="assigned-actions-by-pk"),
    path('', AssignedCreateView.as_view()),
]
