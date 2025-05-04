from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

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
