from django.contrib import admin

from apps.stores.models import AppSection
from apps.stores.models import AppTemplate
from apps.stores.models import Category
from apps.stores.models import Store
from apps.stores.models import StoreTemplates


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
