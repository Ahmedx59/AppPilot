from django.db.models import Sum
from django.utils.timezone import now

from datetime import timedelta

from apps.stores.models import Visit


class VisitService:
    @classmethod
    def visits_store(cls, user_store):
        today = now().date()

        last_days = [today - timedelta(days=x) for x in range(1, 8)]

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

        last_days = [today - timedelta(days=x) for x in range(1, 31)]

        visits = Visit.objects.filter(store=user_store, date__in=last_days)

        result = []
        for _x, day in enumerate(last_days, start=1):
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
    def visits_today(cls, user_store):
        today = now().date()
        visit = Visit.objects.filter(store=user_store, date=today).first()
        return visit.count if visit else 0

    @classmethod
    def total_month_count(cls, user_store):
        today = now().date()
        first_day = today - timedelta(days=30)
        visits = Visit.objects.filter(
            store=user_store,
            date__gte=first_day,
            date__lte=today,
        )
        return visits.aggregate(total=Sum("count"))["total"] or 0
