from django.db import models

from apps.stores.models import Store


class Popup(models.Model):
    name = models.CharField(max_length=50)
    default_setting = models.JSONField()
    code = models.CharField()

    def __str__(self):
        return self.name


class StorePopup(models.Model):
    store = models.ForeignKey(
        Store,
        related_name="store_popup",
        on_delete=models.CASCADE,
    )
    popup = models.ForeignKey(
        Popup,
        related_name="store_popup",
        on_delete=models.CASCADE,
    )
    page_url = models.URLField(max_length=200)
    name = models.CharField(max_length=50, blank=True)
    setting = models.JSONField(blank=True, null=True)
    active = models.BooleanField(default=False)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.popup.name

        if not self.setting:
            self.setting = self.popup.default_setting

        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        from apps.popup.services.popup_services import PopupStoreServices

        PopupStoreServices.activate(self)
        return super().clean()
