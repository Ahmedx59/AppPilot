from apps.stores.models import AppTemplate
from apps.stores.models import Store
from apps.stores.models import StoreTemplates


class StoreServices:
    @classmethod
    def create_store(cls, store, *args, **kwargs):
        Store.objects.create(
            user=store,
            name=store.email,
        )

    @classmethod
    def create_store_template(cls, store, *args, **kwargs):
        for obj in AppTemplate.objects.all():
            StoreTemplates.objects.create(
                app_template=obj,
                section=obj.section,
                components=obj.components,
                order=obj.order,
                is_active=obj.is_active,
                store=store,
            )

    @classmethod
    def backup_store(cls, queryset):
        for store in queryset:
            templates = store.store_templates.all()

            for template in templates:
                template.components_backup = template.components

                template.save()

    @classmethod
    def reset_store(cls, queryset):
        for store in queryset:
            templates = store.store_templates.all()

            for template in templates:
                template.components = template.app_template.components

                template.save()

    @classmethod
    def restore_store(cls, queryset):
        for store in queryset:
            templates = store.store_templates.all()

            for template in templates:
                if template.components_backup:
                    template.components = template.components_backup
                    template.save()
