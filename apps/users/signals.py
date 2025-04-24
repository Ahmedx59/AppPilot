
from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.users.models import User
from apps.stores.models import Store
from apps.stores.services.store_services import StoreServices


@receiver(post_save , sender = User)
def create_store(instance ,created ,*args, **kwargs):
    if created:
        StoreServices().create_store(instance)
