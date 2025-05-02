from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.users.models import User


class Store(models.Model):
    user = models.OneToOneField(User, related_name="store", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    domain = models.CharField(max_length=50, blank=True)
    store_api_key = models.CharField(max_length=50, blank=True)
    applied_date = models.DateField(blank=True, null=True)
    store_hash_value = models.CharField(max_length=50, blank=True)

    notification_service_api_key = models.CharField(max_length=50, blank=True)
    notification_service_auth_key = models.CharField(max_length=50, blank=True)

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    setting_has_changes = models.BooleanField(default=False)
    setting_has_value = models.BooleanField(default=False)
    setting_file = models.FileField(upload_to="store", blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.store_api_key = f"{self.user.id}_{int(timezone.now().timestamp())}"
        return super().save()

    def clean(self):
        if Store.objects.exclude(pk=self.pk).filter(name=self.name).exists():
            raise ValidationError({"name": "This store name is already taken."})
        return super().clean()


class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to="category", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class AppSection(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="section",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to="app_section", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class AppTemplate(models.Model):
    section = models.ForeignKey(
        AppSection,
        related_name="app_template",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to="app_template", blank=True, null=True)
    is_active = models.BooleanField(default=False)
    components = models.JSONField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.clean()

        super().save(*args, **kwargs)

    def clean(self):
        from apps.stores.services.store_services import TemplatesServices

        TemplatesServices().create_template(self)
        return super().clean()


class StoreTemplates(models.Model):
    store = models.ForeignKey(
        Store,
        related_name="store_templates",
        on_delete=models.CASCADE,
    )
    section = models.ForeignKey(
        AppSection,
        related_name="store_templates",
        on_delete=models.CASCADE,
    )
    app_template = models.ForeignKey(
        AppTemplate,
        related_name="store_templates",
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=False)
    components = models.JSONField()
    components_backup = models.JSONField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.app_template.name
