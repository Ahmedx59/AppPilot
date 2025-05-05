from rest_framework.routers import DefaultRouter

from apps.popup.api.views import PopupViewSet
from apps.popup.api.views import StorePopupViewSet

router = DefaultRouter()

router.register("popup", PopupViewSet)
router.register("store_popup", StorePopupViewSet)


urlpatterns = router.urls

app_name = "popup"
