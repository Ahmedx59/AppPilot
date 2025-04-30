from rest_framework import serializers

from apps.stores.models import AppSection
from apps.stores.models import Category
from apps.stores.models import StoreTemplates
from apps.stores.services.store_services import TemplatesServices


class AppSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppSection
        fields = ("name", "icon", "order")


class CategorySerializer(serializers.ModelSerializer):
    section = AppSectionSerializer(many=True)

    class Meta:
        model = Category
        fields = ("name", "icon", "order", "section")


class StoreTemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreTemplates
        fields = "__all__"


class UpdateStoreTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreTemplates
        fields = ("components",)


class ActivateTemplateSerializer(serializers.Serializer):
    def save(self, **kwargs):
        user = self.context["request"].user
        section_id = self.context["view"].kwargs["section_id"]
        template_id = self.context["view"].kwargs["pk"]

        TemplatesServices().activate_template(user, section_id, template_id)


class GeneralizeSerializer(serializers.Serializer):
    def save(self, **kwargs):
        user = self.context["request"].user
        section_id = self.context["view"].kwargs["section_id"]
        template_id = self.context["view"].kwargs["pk"]

        TemplatesServices().generalize_template(user, section_id, template_id)
