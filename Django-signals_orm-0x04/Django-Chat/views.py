from django.shortcuts import render
from messaging.models import Message
from django.db.models import Prefetch

def conversation_view(request):
    root_messages = Message.objects.filter(parent_message__isnull=True).select_related(
        'sender', 'receiver'
    ).prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    )
    return render(request, 'chat/conversation.html', {'messages': root_messages})
