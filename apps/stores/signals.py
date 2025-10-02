from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.stores.models import Store
from apps.stores.models import StoreTemplates
from apps.stores.services.store_services import StoreServices
from apps.stores.services.template_services import ComponentsService


@receiver(post_save, sender=Store)
def create_store_template(instance, created, *args, **kwargs):
    if created:
        StoreServices.create_store_template(instance)


# @receiver(post_save, sender=StoreTemplates)
# def check_components(instance, created, *args, **kwargs):
#     if created:
#         TemplatesServices.check_components(instance, StoreTemplates)


@receiver(pre_save, sender=StoreTemplates)
def store_old_components(sender, instance, **kwargs):
    ComponentsService.store_old_components(instance)


@receiver(post_save, sender=StoreTemplates)
def check_components_after_save(sender, instance, created, **kwargs):
    ComponentsService.check_components_after_save(instance, created)
