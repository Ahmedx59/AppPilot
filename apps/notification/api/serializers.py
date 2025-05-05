from rest_framework import serializers

from apps.notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("title", "message", "url", "sent_at", "created_at","is_published",)


class UpdateCreateNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("title","message","url",)

        
    def create(self, validated_data):
        validated_data["store"] = self.context["request"].user.store
        return super().create(validated_data)
