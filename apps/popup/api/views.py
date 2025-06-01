from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.popup.api.serializers import DuplicateStorePopupSerializer
from apps.popup.api.serializers import PopupSerializer
from apps.popup.api.serializers import ResetStorePopupSerializer
from apps.popup.api.serializers import StorePopupSerializer
from apps.popup.api.serializers import UpdateCreateStorePopupSerializer
from apps.popup.models import Popup
from apps.popup.models import StorePopup


class StorePopupViewSet(viewsets.ModelViewSet):
    queryset = StorePopup.objects.all()
    serializer_class = StorePopupSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ["create", "update", "partial_update"]:
            return UpdateCreateStorePopupSerializer

        return super().get_serializer_class(*args, **kwargs)

    def get_queryset(self):
        user_store = self.request.user.store
        return super().get_queryset().filter(store=user_store)

    @extend_schema(request=None, responses=DuplicateStorePopupSerializer)
    @action(detail=True, methods=["post"])
    def duplicate(self, request, pk=None):
        store_popup = self.get_object()
        serializer = DuplicateStorePopupSerializer(
            data={},
            context={"store_popup": store_popup},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(request=None, responses=StorePopupSerializer)
    @action(detail=True, methods=["post"])
    def reset(self, request, pk=None):
        store_popup = self.get_object()
        serializer = ResetStorePopupSerializer(
            data={},
            context={"store_popup": store_popup},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PopupViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Popup.objects.all()
    serializer_class = PopupSerializer
