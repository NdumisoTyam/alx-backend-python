from django.shortcuts import render
from messaging.models import Message
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

@login_required
def inbox_view(request):
    unread_messages = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'timestamp')
    return render(request, 'chat/inbox.html', {'unread_messages': unread_messages})

def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        receiver_id = request.POST.get('receiver')
        parent_id = request.POST.get('parent_message')

        receiver = User.objects.get(id=receiver_id)
        parent_message = Message.objects.get(id=parent_id) if parent_id else None

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_message
        )

    messages = Message.objects.filter(parent_message__isnull=True).select_related(
        'sender', 'receiver'
    ).prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    )

    return render(request, 'chat/threaded_messages.html', {'messages': messages})

def get_thread(message):
    thread = [message]
    for reply in message.replies.select_related('sender', 'receiver').all():
        thread.extend(get_thread(reply))
    return thread
