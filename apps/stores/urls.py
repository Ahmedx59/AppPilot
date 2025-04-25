# from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.stores.api.views import CategoryViewSet

router = DefaultRouter()
router.register("category", CategoryViewSet, basename="category")

urlpatterns = router.urls

app_name = "stores"
