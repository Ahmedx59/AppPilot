from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# from apps.stores.api.serializers import AppSectionSerializer
from apps.stores.api.serializers import ActivateTemplateSerializer
from apps.stores.api.serializers import CategorySerializer
from apps.stores.api.serializers import GeneralizeSerializer
from apps.stores.api.serializers import StoreTemplatesSerializer
from apps.stores.api.serializers import UpdateStoreTemplateSerializer
from apps.stores.api.serializers import VisitSerializer
from apps.stores.models import Category
from apps.stores.models import StoreTemplates
from apps.stores.models import Visit


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StoreTemplatesViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = StoreTemplates.objects.all()
    serializer_class = StoreTemplatesSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "update":
            return UpdateStoreTemplateSerializer
        return super().get_serializer_class(*args, **kwargs)

    def get_queryset(self):
        user_store = self.request.user.store

        queryset = super().get_queryset()

        section_id = self.kwargs["section_id"]
        # section = AppSection.objects.get(id=section_id)
        return queryset.filter(section_id=section_id, store=user_store)

    @action(detail=True, methods=["post"], serializer_class=ActivateTemplateSerializer)
    def activate(self, request, section_id, pk):
        serializer = self.get_serializer(data={})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Template activated successfully."})

    @action(detail=True, methods=["post"], serializer_class=GeneralizeSerializer)
    def generalize(self, request, section_id, pk):
        serializer = self.get_serializer(data={})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Components generalized to other templates."},
            status=status.HTTP_200_OK,
        )


class StoreViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    pagination_class = None

    @action(detail=True, methods=["get"])
    def visit(self, request, *args, **kwargs):
        user_store = request.user.store
        serializer = self.get_serializer(user_store)
        return Response(serializer.data)
