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
        fields = ("id", "popup", "active", "setting", "page_url", "name", "updated_at")
        # exclude = ("store","updated_at",)


class UpdateCreateStorePopupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorePopup
        exclude = ("store", "updated_at")

    def create(self, validated_data):
        validated_data["store"] = self.context["request"].user.store
        return super().create(validated_data)


class DuplicateStorePopupSerializer(serializers.Serializer):
    def create(self, validated_data):
        store_popup = self.context["store_popup"]
        store_popup.pk = None
        store_popup.active = False
        store_popup.save()
        return store_popup

    def to_representation(self, instance):
        return StorePopupSerializer(instance).data


class ResetStorePopupSerializer(serializers.Serializer):
    def create(self, validated_data):
        store_popup = self.context["store_popup"]
        store_popup.setting = store_popup.popup.default_setting
        store_popup.active = False
        store_popup.save()
        return store_popup

    def to_representation(self, instance):
        return StorePopupSerializer(instance).data
