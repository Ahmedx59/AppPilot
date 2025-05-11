from django.contrib import admin

from apps.notification.models import Notification


@admin.register(Notification)
class AdminNotification(admin.ModelAdmin):
    list_display = ("title", "id")
    list_filter = ("title", "id")
