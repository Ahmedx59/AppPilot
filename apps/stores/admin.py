from django.contrib import admin

from apps.stores.models import (
    Store,
    Category,
    AppSection,
    AppTemplate,
    StorTemplates,
    )

@admin.register(Store)
class AdminStore(admin.ModelAdmin):
    list_display = ('user','name')
    list_filter = ('user','name')


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)




@admin.register(AppSection)
class AdminAppSection(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)



@admin.register(AppTemplate)
class AdminAppSection(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)




@admin.register(StorTemplates)
class AdminStorTemplates(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
