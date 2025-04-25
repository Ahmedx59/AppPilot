from rest_framework import serializers

from apps.stores.models import AppSection
from apps.stores.models import Category


class AppSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppSection
        fields = ("name", "icon", "order")


class CategorySerializer(serializers.ModelSerializer):
    section = AppSectionSerializer(many=True)

    class Meta:
        model = Category
        fields = ("name", "icon", "order", "section")
