from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from apps.stores.models import Store
from apps.stores.models import StoreTemplates

# ruff: noqa: SLF001


class TemplatesServices:
    @classmethod
    def create_template(cls, app_template, model, store=None):
        if app_template.pk:
            prev = model.objects.get(pk=app_template.pk)
            if prev.is_active and not app_template.is_active:
                raise ValidationError(
                    {
                        "is_active": "You can't deactivate the active template."
                        "You must activate another one instead.",
                    },
                )
        if store:
            query = model.objects.filter(
                is_active=True,
                section=app_template.section,
                store=app_template.store,
            ).exclude(pk=app_template.pk)
        else:
            query = model.objects.filter(
                is_active=True,
                section=app_template.section,
            ).exclude(pk=app_template.pk)

        if app_template.is_active:
            query.update(is_active=False)

        cls.templates_create(app_template, model, query, store)

    @staticmethod
    def templates_create(app_template, model, query, store):
        if not (query.exists()) and not app_template.is_active:
            raise ValidationError(
                {"is_active": "must be one active template per section"},
            )

    @classmethod
    def activate_template(cls, user, section_id, template_id):
        user_store = user.store

        template_to_activate = get_object_or_404(
            StoreTemplates,
            id=template_id,
            section_id=section_id,
            store=user_store,
        )

        StoreTemplates.objects.filter(
            section=section_id,
            store=user_store,
        ).exclude(id=template_id).update(is_active=False)

        template_to_activate.is_active = True
        template_to_activate.save()

        return template_to_activate

    @classmethod
    def generalize_template(cls, user, section_id, template_id):
        user_store = user.store

        source_template = get_object_or_404(
            StoreTemplates,
            id=template_id,
            section_id=section_id,
            store=user_store,
        )

        copied_components = source_template.components

        templates_to_update = StoreTemplates.objects.filter(
            section_id=section_id,
            store=user_store,
        ).exclude(id=template_id)

        for template in templates_to_update:
            template.components_backup = template.components
            template.components = copied_components
            template.save()

    @classmethod
    def restore_template(cls, template):
        if template.components_backup:
            template.components = template.components_backup
            template.save()

    @classmethod
    def check_components(cls, template, model):
        if template.components.pk:
            component = model.object.get(pk=template.components.pk)
            if template.components.pk != component:
                template.store.setting_has_changes = True
                template.save()


class ComponentsService:
    @staticmethod
    def store_old_components(instance):
        if instance.pk:
            try:
                old_instance = instance.__class__.objects.get(pk=instance.pk)
                instance._old_components = old_instance.components
            except instance.__class__.DoesNotExist:
                instance._old_components = None
        else:
            instance._old_components = None

    @staticmethod
    def check_components_after_save(instance, created):
        if not created and hasattr(instance, "_old_components"):
            if instance._old_components != instance.components:
                Store.objects.filter(pk=instance.store.pk).update(
                    setting_has_changes=True,
                )

    @staticmethod
    def store_components(instance):
        if instance.pk:
            try:
                old_instance = instance.__class__.objects.get(pk=instance.pk)
                instance._old_components = old_instance.components
            except instance.__class__.DoesNotExist:
                instance._old_components = None
        else:
            instance._old_components = None
