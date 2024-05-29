import django_filters
from django_filters import OrderingFilter

from pulse.models import Project


class ProjectFilter(django_filters.FilterSet):
    order_by_field = 'orderBy'
    order_by = OrderingFilter(
        fields=("id", "name", "start_date", "end_date", "income",)
    )

    class Meta:
        model = Project
        fields = ["id", "name", "start_date", "end_date", "income"]
