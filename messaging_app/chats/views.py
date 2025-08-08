from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email', 'participants__first_name', 'participants__last_name']

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participant_ids')
        if not participant_ids or not isinstance(participant_ids, list):
            return Response({"error": "participant_ids must be a list of user IDs."},
                            status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() != len(participant_ids):
            return Response({"error": "One or more user IDs are invalid."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body', 'sender__email']

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')

        if not conversation_id or not message_body:
            return Response({"error": "conversation_id and message_body are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        sender = request.user

        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
