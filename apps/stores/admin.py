from django.contrib import admin

from apps.stores.models import AppSection
from apps.stores.models import AppTemplate
from apps.stores.models import Category
from apps.stores.models import Store
from apps.stores.models import StoreTemplates
from apps.stores.models import Visit


class AppTemplateInline(admin.TabularInline):
    model = AppTemplate


class AppSectionInline(admin.TabularInline):
    model = AppSection


@admin.register(Store)
class AdminStore(admin.ModelAdmin):
    list_display = ("user", "name")
    list_filter = ("user", "name")


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    inlines = (AppSectionInline,)


@admin.register(AppSection)
class AdminAppSection(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    inlines = (AppTemplateInline,)


@admin.register(AppTemplate)
class AdminAppTemplate(admin.ModelAdmin):
    list_display = ("name", "section", "is_active", "order")
    list_filter = ("name", "section", "is_active", "order")


@admin.register(StoreTemplates)
class AdminStorTemplates(admin.ModelAdmin):
    list_display = ("store", "id", "section", "app_template", "is_active", "order")
    list_filter = ("store", "id", "section", "app_template", "is_active", "order")
    actions = ("backup_components",)

    def backup_components(self, request, queryset):
        try:
            count = 0
            for obj in queryset:
                obj.components_backup = obj.components
                obj.save()
                count += 1
            self.message_user(request, f"✅ Backup completed for {count} template(s).")
        except Exception as e:
            self.message_user(request, f"❌ An error occurred: {e}")
            raise


@admin.register(Visit)
class AdminVisit(admin.ModelAdmin):
    list_display = ("date",)
    list_filter = ("date",)
