from django.urls import path

from pulse.views.employee import EmployeeCreateView, EmployeeDetailView, \
    EmployeeDetailViewAddToCompany

urlpatterns = [
    path('/<int:pk>', EmployeeDetailView.as_view(), name="employee-actions-by-pk"),
    path('', EmployeeCreateView.as_view()),
    path('/invite', EmployeeDetailViewAddToCompany.as_view())
]
