from django.urls import path

from pulse.views.employee import EmployeeCreateView, EmployeeListView, EmployeeDetailView

urlpatterns = [
    path('/search', EmployeeListView.as_view()),
    path('/<int:pk>', EmployeeDetailView.as_view(), name="employee-actions-by-pk"),
    path('', EmployeeCreateView.as_view()),
]
