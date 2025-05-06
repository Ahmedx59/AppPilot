from rest_framework.routers import DefaultRouter

from apps.notification.api.views import NotificationViewSet

router = DefaultRouter()

router.register("notification", NotificationViewSet)

urlpatterns = router.urls

app_name = "notification"
