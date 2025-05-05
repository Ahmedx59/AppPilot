from rest_framework import viewsets

from apps.notification.api.serializers import NotificationSerializer , UpdateCreateNotificationSerializer
from apps.notification.models import Notification


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ["create", "update", "partial_update"]:
            return UpdateCreateNotificationSerializer

        return super().get_serializer_class(*args, **kwargs)

    def get_queryset(self):
        user_store = self.request.user.store
        return super().get_queryset().filter(store=user_store)
    