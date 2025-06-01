from rest_framework import serializers

from apps.stores.models import AppSection
from apps.stores.models import Category
from apps.stores.models import StoreTemplates
from apps.stores.services.store_services import TemplatesServices
from apps.stores.services.store_services import VisitService


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

        TemplatesServices.activate_template(user, section_id, template_id)


class GeneralizeSerializer(serializers.Serializer):
    def save(self, **kwargs):
        user = self.context["request"].user
        section_id = self.context["view"].kwargs["section_id"]
        template_id = self.context["view"].kwargs["pk"]

        TemplatesServices.generalize_template(user, section_id, template_id)


class VisitSerializer(serializers.Serializer):
    filter_days = serializers.SerializerMethodField()
    today = serializers.SerializerMethodField()
    month_total = serializers.SerializerMethodField()

    def get_filter_days(self, obj):
        self.user_store = self.context["request"].user.store
        filter_type = self.context.get("day") or "daily"

        if filter_type == "daily":
            return VisitService.visits_store(self.user_store)

        if filter_type == "month":
            return VisitService.visits_store_month(self.user_store)

        return {"error": "Invalid filter type"}

    def get_today(self, *args, **kwargs):
        return VisitService.visits_today(self.user_store)

    def get_month_total(self, *args, **kwargs):
        return VisitService.total_month_count(self.user_store)
