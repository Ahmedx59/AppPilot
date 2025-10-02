from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from apps.notification.api.serializers import DuplicateNotificationSerializer
from apps.notification.api.serializers import NotificationSerializer
from apps.notification.api.serializers import UpdateCreateNotificationSerializer
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

    def perform_destroy(self, instance):
        if instance.is_published:
            raise ValidationError(
                {"message": "A published notification cannot be deleted."},
            )
        instance.delete()
        return Response(
            {"message": "Notification deleted successfully."},
            status=status.HTTP_200_OK,
        )

    # @extend_schema(request=None, responses=DuplicateNotificationSerializer)
    @action(
        detail=True,
        methods=["post"],
        serializer_class=DuplicateNotificationSerializer,
    )
    def duplicate(self, request, pk=None):
        notification = self.get_object()

        if notification.is_published:
            return Response(
                {
                    "message": "This notification is already published"
                    "and cannot be copied.",
                },
                status=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(
            data={},
            context={"notification": notification},
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
