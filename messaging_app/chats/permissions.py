from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only authenticated users who are participants
    of a conversation to send, view, update, or delete messages.
    """

    SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]
    WRITE_METHODS = ["POST", "PUT", "PATCH", "DELETE"]

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant of the conversation
        conversation = getattr(obj, 'conversation', obj)

        if request.method in self.WRITE_METHODS or request.method in self.SAFE_METHODS:
            return request.user in conversation.participants.all()

        # Deny other methods by default
        return False

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
