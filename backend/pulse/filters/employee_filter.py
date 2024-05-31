import django_filters
from django_filters import OrderingFilter

from pulse.models import Employee


class EmployeeFilter(django_filters.FilterSet):
    order_by_field = 'orderBy'
    order_by = OrderingFilter(
        fields=("id", "user", "company",)
    )

    class Meta:
        model = Employee
        fields = ["id", "user", "company", "is_project_manager", "disabled"]
