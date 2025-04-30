# from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.stores.api.views import CategoryViewSet
from apps.stores.api.views import StoreTemplatesViewSet

router = DefaultRouter()

router.register("category", CategoryViewSet, basename="category")
router.register(
    r"section/(?P<section_id>\d+)/template",
    StoreTemplatesViewSet,
    basename="templates",
)


urlpatterns = router.urls

app_name = "stores"
