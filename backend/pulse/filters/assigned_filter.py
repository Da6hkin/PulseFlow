import django_filters
from django_filters import OrderingFilter

from pulse.models import Assigned


class AssignedFilter(django_filters.FilterSet):
    order_by_field = 'orderBy'
    order_by = OrderingFilter(
        fields=("id", "task", "employee", "rate_type", "rate",)
    )

    class Meta:
        model = Assigned
        fields = ["id", "task", "employee", "rate_type", "rate"]