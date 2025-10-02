from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.stores.services.store_services import StoreServices
from apps.users.models import User


@receiver(post_save, sender=User)
def create_store(instance, created, *args, **kwargs):
    if created:
        StoreServices.create_store(instance)
