from rest_framework import serializers

from apps.notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("title", "message", "url", "sent_at", "created_at", "is_published")


class UpdateCreateNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("title", "message", "url")

    def create(self, validated_data):
        validated_data["store"] = self.context["request"].user.store
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.is_published:
            raise serializers.ValidationError(
                {"message": ("A published notification cannot be edited.")},
            )
        return super().update(instance, validated_data)


class DuplicateNotificationSerializer(serializers.Serializer):
    def create(self, validated_data):
        notification = self.context["notification"]

        notification.pk = None
        notification.is_published = False
        notification.save()

        return notification

    def to_representation(self, instance):
        return NotificationSerializer(instance).data
