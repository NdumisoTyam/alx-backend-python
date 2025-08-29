def get_thread(message):
    thread = [message]
    for reply in message.replies.select_related('sender', 'receiver').all():
        thread.extend(get_thread(reply))
    return thread
