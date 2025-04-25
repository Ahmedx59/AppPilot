from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.stores.models import Store
from apps.stores.services.store_services import StoreServices


@receiver(post_save, sender=Store)
def create_store_template(instance, created, *args, **kwargs):
    if created:
        StoreServices().create_store_template(instance)
