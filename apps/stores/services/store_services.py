from apps.stores.models import AppTemplate
from apps.stores.models import Store
from apps.stores.models import StorTemplates


class StoreServices:
    def create_store(self, instance, *args, **kwargs):
        Store.objects.create(
            user=instance,
            name=instance.email,
        )

    def create_store_template(self, store, *args, **kwargs):
        for object in AppTemplate.objects.all():
            StorTemplates.objects.create(
                app_template=object,
                section=object.section,
                components=object.components,
                order=object.order,
                is_active=object.is_active,
                store=Store,
            )
