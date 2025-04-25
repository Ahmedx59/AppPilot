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
        for obj in AppTemplate.objects.all():
            StorTemplates.objects.create(
                app_template=obj,
                section=obj.section,
                components=obj.components,
                order=obj.order,
                is_active=obj.is_active,
                store=store,
            )
