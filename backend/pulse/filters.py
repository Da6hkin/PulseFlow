from django_filters import rest_framework as filters, CharFilter, BooleanFilter

from pulse.models import User


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'is_admin']
