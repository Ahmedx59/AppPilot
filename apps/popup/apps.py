import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "apps.popup"
    verbose_name = _("Popup")

    def ready(self):
        with contextlib.suppress(ImportError):
            import apps.popup.signals  # noqa: F401
