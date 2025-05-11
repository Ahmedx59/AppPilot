# from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.stores.api.views import CategoryViewSet
from apps.stores.api.views import StoreTemplatesViewSet
from apps.stores.api.views import StoreViewSet

router = DefaultRouter()

router.register("category", CategoryViewSet, basename="category")
router.register("store", StoreViewSet, basename="store")
router.register(
    r"section/(?P<section_id>\d+)/template",
    StoreTemplatesViewSet,
    basename="templates",
)


urlpatterns = router.urls

app_name = "stores"
