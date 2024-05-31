import django_filters
from django_filters import OrderingFilter

from pulse.models import Company


class CompanyFilter(django_filters.FilterSet):
    order_by_field = 'orderBy'
    order_by = OrderingFilter(
        fields=("id", "name", "unique_identifier",)
    )

    class Meta:
        model = Company
        fields = ["id", "name", "unique_identifier", "website"]
