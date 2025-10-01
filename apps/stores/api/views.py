from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# from apps.stores.api.serializers import AppSectionSerializer
from apps.stores.api.serializers import ActivateTemplateSerializer
from apps.stores.api.serializers import CategoryListSerializer
from apps.stores.api.serializers import CategorySerializer
from apps.stores.api.serializers import GeneralizeTemplateSerializer
from apps.stores.api.serializers import StoreTemplatesSerializer
from apps.stores.api.serializers import UpdateStoreTemplateSerializer
from apps.stores.api.serializers import VisitSerializer
from apps.stores.models import Category
from apps.stores.models import StoreTemplates
from apps.stores.models import Visit
from apps.stores.services.template_services import TemplatesServices


class CategoryViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.filter(is_meta=False)
    serializer_class = CategorySerializer

    @action(detail=False, methods=["get"], serializer_class=CategoryListSerializer)
    def is_meta(self, request):
        queryset = Category.objects.filter(is_meta=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema("Templates")
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

    @action(
        detail=True,
        methods=["post"],
        serializer_class=GeneralizeTemplateSerializer,
    )
    def generalize(self, request, section_id, pk):
        serializer = self.get_serializer(data={})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Components generalized to other templates."},
            status=status.HTTP_200_OK,
        )


    @action(detail=True, methods=["post"], serializer_class=None)
    def restore(self, *args, **kwargs):
        template = self.get_object()
        TemplatesServices.restore_template(template)
        return Response({"detail": "Template Restore completed"})


class StoreViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    pagination_class = None

    @action(detail=True, methods=["get"])
    def visit(self, request, *args, **kwargs):
        day = self.request.query_params.get("filter_day_monthly")
        user_store = request.user.store
        serializer = self.get_serializer(
            user_store,
            context={"day": day, "request": request},
        )
        return Response(serializer.data)
