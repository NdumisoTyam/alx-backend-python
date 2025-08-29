from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification
from .models import Message, MessageHistory

class SignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')

    def test_notification_created_on_message(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello!')
        notif = Notification.objects.filter(user=self.receiver, message=msg)
        self.assertEqual(notif.count(), 1)

class MessageEditSignalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, content='Original')

    def test_edit_logs_history(self):
        self.message.content = 'Updated'
        self.message.save()
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, 'Original')

