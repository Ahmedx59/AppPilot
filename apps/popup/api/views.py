from rest_framework import mixins
from rest_framework import viewsets

from apps.popup.api.serializers import PopupSerializer
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


class PopupViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Popup.objects.all()
    serializer_class = PopupSerializer
