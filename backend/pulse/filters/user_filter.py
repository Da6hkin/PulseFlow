import django_filters
from django_filters import OrderingFilter

from pulse.models import User


class UserFilter(django_filters.FilterSet):
    order_by_field = 'orderBy'
    order_by = OrderingFilter(
        fields=("id",)
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'disabled']
