import django_filters
from django_filters import OrderingFilter

from pulse.models import ProjectManager


class ProjectManagerFilter(django_filters.FilterSet):
    order_by_field = 'orderBy'
    order_by = OrderingFilter(
        fields=("id", "employee", "project",)
    )

    class Meta:
        model = ProjectManager
        fields = ["id", "employee", "project", "disabled"]
