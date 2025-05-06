import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationsConfig(AppConfig):
    name = "apps.notification"
    verbose_name = _("Notification")

    def ready(self):
        with contextlib.suppress(ImportError):
            import apps.notification.signals  # noqa: F401
