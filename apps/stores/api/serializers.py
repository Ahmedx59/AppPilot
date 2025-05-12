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
    per_day = serializers.SerializerMethodField()
    per_month = serializers.SerializerMethodField()
    today = serializers.SerializerMethodField()
    month_total = serializers.SerializerMethodField()

    def get_per_day(self, *args, **kwargs):
        user_store = self.context["request"].user.store
        return VisitService.visits_store(user_store)
    
    def get_per_month(self, *args, **kwargs):
        user_store = self.context["request"].user.store
        return VisitService.visits_store_month(user_store)
    
    def get_today(self, *args, **kwargs):
        user_store = self.context["request"].user.store
        return VisitService.visits_today(user_store)

    def get_month_total(self, *args, **kwargs):
        user_store = self.context["request"].user.store
        return VisitService.total_month_count(user_store)
