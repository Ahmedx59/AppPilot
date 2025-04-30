from django.db import models

from apps.stores.models import Store


class StorePopup(models.Model):
    store_id = models.ForeignKey(
        Store,
        related_name="store_popup",
        on_delete=models.CASCADE,
    )
    plugin_id = ""
    page_url = ""
    name = models.CharField(max_length=50)
    setting = models.JSONField()
    active = models.BooleanField(default=False)
    updated_at = ""

    def __str__(self):
        return self.name


class Popup(models.Model):
    store_popup = models.ForeignKey(
        StorePopup,
        related_name="popup",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    default_setting = models.JSONField()
    code = models.CharField()

    def __str__(self):
        return self.name
