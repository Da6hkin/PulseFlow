import django_filters
from django_filters import OrderingFilter

from pulse.models import ChatMessage


class ChatMessageFilter(django_filters.FilterSet):
    order_by_field = 'orderBy'
    order_by = OrderingFilter(
        fields=("id", "project", "text", "user", "created_at",)
    )

    class Meta:
        model = ChatMessage
        fields = ["id", "project", "text", "user", "created_at"]
