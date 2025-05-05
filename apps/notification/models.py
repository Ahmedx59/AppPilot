from django.db import models

from apps.stores.models import Store


class Notification(models.Model):
    store = models.ForeignKey(
        Store,
        related_name="notification",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=50)
    url = models.URLField(max_length=200)
    sent_at = models.DateField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True , blank=True, null=True)

    def __str__(self):
        return self.title
