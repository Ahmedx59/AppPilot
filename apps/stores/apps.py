import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StoresConfig(AppConfig):
    name = "apps.stores"
    verbose_name = _("Stores")

    def ready(self):
        with contextlib.suppress(ImportError):
            import apps.stores.signals  # noqa: F401
