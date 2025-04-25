from rest_framework import mixins
from rest_framework import viewsets

# from apps.stores.api.serializers import AppSectionSerializer
from apps.stores.api.serializers import CategorySerializer
from apps.stores.models import Category


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
