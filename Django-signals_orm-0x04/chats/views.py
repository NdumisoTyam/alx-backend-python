from django.views.decorators.cache import cache_page
from django.shortcuts import render
from messaging.models import Message
from django.urls import path
from chats.views import conversation_view

@cache_page(60)  # ⏱️ Cache for 60 seconds
def conversation_view(request, conversation_id):
    messages = Message.objects.filter(parent_message_id=conversation_id).order_by('timestamp')
    return render(request, 'chat/conversation.html', {'messages': messages})

urlpatterns = [
    path('conversation/<int:conversation_id>/', conversation_view, name='conversation'),
]
