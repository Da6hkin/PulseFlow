from django.urls import path

from pulse.views.chat_message import ChatMessageListView, ChatMessageCreateView

urlpatterns = [
    path('/search', ChatMessageListView.as_view()),
    path('', ChatMessageCreateView.as_view()),
]
