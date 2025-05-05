from rest_framework import serializers

from apps.popup.models import Popup
from apps.popup.models import StorePopup


class PopupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Popup
        fields = "__all__"


class StorePopupSerializer(serializers.ModelSerializer):
    popup = PopupSerializer()

    class Meta:
        model = StorePopup
        fields = ("popup", "active", "setting", "page_url", "name", "updated_at")
        # exclude = ("store","updated_at",)


class UpdateCreateStorePopupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorePopup
        exclude = ("store", "updated_at")

    def create(self, validated_data):
        validated_data["store"] = self.context["request"].user.store
        return super().create(validated_data)
