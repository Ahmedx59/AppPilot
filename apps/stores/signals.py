
from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.users.models import User
from apps.stores.models import Store


@receiver(post_save , sender = User)
def owner(instance ,created ,*args, **kwargs):
    if created:
        Store.objects.create(
            user = instance,
            name = instance.email
        )