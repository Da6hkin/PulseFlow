from django.urls import path

from pulse.views.chat_message import ChatMessageListView, ChatMessageDetailView, ChatMessageCreateView

urlpatterns = [
    path('/search', ChatMessageListView.as_view()),
    path('/<int:pk>', ChatMessageDetailView.as_view(), name="chat-message-actions-by-pk"),
    path('', ChatMessageCreateView.as_view()),
]
