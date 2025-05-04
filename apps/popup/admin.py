from django.contrib import admin

from apps.popup.models import Popup
from apps.popup.models import StorePopup


@admin.register(StorePopup)
class AdminStorePopup(admin.ModelAdmin):
    list_display = ("name", "store", "active")
    list_filter = ("name", "store", "active")


@admin.register(Popup)
class AdminPopup(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
