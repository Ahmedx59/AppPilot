from datetime import timedelta

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.db.models import Sum

from apps.stores.models import AppTemplate
from apps.stores.models import Store
from apps.stores.models import StoreTemplates
from apps.stores.models import Visit


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


class VisitService:
    @classmethod
    def visits_store(cls, user_store):
        today = now().date()

        last_days = [today - timedelta(days=x) for x in range(1,8)]

        visits = Visit.objects.filter(store=user_store, date__in=last_days)

        result = []
        for day in last_days:
            visits_by_date = visits.filter(date=day).first()

            if visits_by_date:
                result.append(
                    {
                        "date": visits_by_date.date,
                        "count": visits_by_date.count,
                    },
                )

            else:
                result.append(
                    {
                        "date": day,
                        "count": 0,
                    },
                )
        return result
    
    @classmethod
    def visits_store_month(cls, user_store):
        today = now().date()

        last_days = [today - timedelta(days=x) for x in range(1,31)]

        visits = Visit.objects.filter(store=user_store, date__in=last_days)

        result = []
        x = 0
        for day in last_days:
            x += 1
            visits_by_date = visits.filter(date=day).first()

            if visits_by_date:
                result.append(
                    {
                        "date": visits_by_date.date,
                        "count": visits_by_date.count,
                    },
                )

            else:
                result.append(
                    {
                        "date": day,
                        "count": 0,
                    },
                )

        result.append(
            {
                "count":x,
            }
        )
        return result 
    
    @classmethod
    def visits_today(cls, user_store):
        today = now().date()
        visit = Visit.objects.filter(store=user_store, date=today).first()
        return {"date": today, "count": visit.count if visit else 0}

    @classmethod
    def total_month_count(cls, user_store):
        today = now().date()
        first_day = today - timedelta(days=30)
        visits = Visit.objects.filter(store=user_store, date__gte=first_day, date__lte=today)
        total = visits.aggregate(total=Sum("count"))["total"] or 0
        return total