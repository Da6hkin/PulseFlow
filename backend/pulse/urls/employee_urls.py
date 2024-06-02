from django.urls import path

from pulse.views.employee import EmployeeCreateView, EmployeeDetailView, \
    EmployeeDetailViewAddToCompany, EmployeeListView

urlpatterns = [
    path('/search', EmployeeListView.as_view()),
    path('/<int:pk>', EmployeeDetailView.as_view(), name="employee-actions-by-pk"),
    path('', EmployeeCreateView.as_view()),
    path('/invite', EmployeeDetailViewAddToCompany.as_view())
]
