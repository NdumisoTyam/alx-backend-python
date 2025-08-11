from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone_number',
            'role',
            'created_at',
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.CharField(source='sender.email', read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender_email',
            'message_body',
            'sent_at',
        ]

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages',
        ]

    def get_messages(self, obj):
        messages = obj.messages.order_by('sent_at')
        return MessageSerializer(messages, many=True).data

