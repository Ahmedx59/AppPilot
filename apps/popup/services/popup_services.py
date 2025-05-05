from django.core.exceptions import ValidationError

from apps.popup.models import StorePopup


class PopupStoreServices:
    @classmethod
    def activate(cls, store_popup):
        if store_popup.active:
            active_popup = StorePopup.objects.filter(
                active=True,
                store=store_popup.store,
            ).count()
            if active_popup >= 3:  # noqa:PLR2004
                raise ValidationError({"active": "you can activate 3 popup only."})


# class PopupStoreServices:

#     # def __init__(self, outer_queryset):
#     #     self.queryset = outer_queryset


#     @classmethod
#     def activate(cls, store_popup ,hjf):
#         cls.test()
#         cls.generate(store_popup)
#         # self.queryset.filter(name="ds")


#     def test(self):
#         print(self.queryset)


#     @staticmethod
#     def generate(store_popup):
#          if store_popup.active:
#             active_popup = StorePopup.objects.filter
#               (active=True , store = store_popup.store).count()
#             if active_popup >= 3:
#                 raise ValidationError({"active": "you can activate 3 popup only."})
