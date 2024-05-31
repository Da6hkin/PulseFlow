import django_filters
from django_filters import OrderingFilter

from pulse.models import Task


class TaskFilter(django_filters.FilterSet):
    order_by_field = 'orderBy'
    order_by = OrderingFilter(
        fields=("id", "name", "state", "priority", "planned_start_date", "planned_end_date", )
    )

    class Meta:
        model = Task
        fields = ["id", "name", "project", "state", "priority", "planned_end_date"]
