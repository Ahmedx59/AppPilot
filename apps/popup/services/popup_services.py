from django.core.exceptions import ValidationError

from apps.popup.models import StorePopup


class PopupStoreServices:
    def activate(self,store_popup):
        if store_popup.active:
            active_popup = StorePopup.objects.filter(active=True , store = store_popup.store).count()
            if active_popup >= 3:  # noqa:PLR2004
                raise ValidationError({"active": "you can activate 3 popup only."})
