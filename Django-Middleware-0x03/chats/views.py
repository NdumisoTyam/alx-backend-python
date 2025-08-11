from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
     pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        conversation_id = self.request.query_params.get("conversation_id")
        queryset = Message.objects.filter(conversation__participants=self.request.user)
        if conversation_id:
            return Message.objects.filter(
                conversation__id=conversation_id,
                conversation__participants=self.request.user
            )
        return Message.objects.filter(conversation__participants=self.request.user)
        queryset = queryset.filter(conversation__id=conversation_id)
        return queryset

    def perform_create(self, serializer):
        conversation_id = self.request.data.get("conversation_id")
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not allowed to send messages in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save(sender=self.request.user, conversation=conversation)

    def perform_update(self, serializer):
        message = self.get_object()
        if self.request.user not in message.conversation.participants.all():
            return Response(
                {"detail": "You are not allowed to update this message."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user not in instance.conversation.participants.all():
            return Response(
                {"detail": "You are not allowed to delete this message."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()

