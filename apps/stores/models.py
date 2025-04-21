from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models

from apps.users.models import User



class Store(models.Model):
    user = models.OneToOneField(User, related_name='store', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    store_api_key = models.CharField(max_length=50)
    applied_date = models.DateField()
    store_hash_value = models.CharField(max_length=50)

    notification_service_api_key = models.CharField(max_length=50)
    notification_service_auth_key = models.CharField(max_length=50)

    created = models.DateField(auto_now_add=True)
    udated = models.DateField(auto_now=True)

    setting_has_changes = models.BooleanField()
    setting_has_value = models.BooleanField()
    setting_file = models.FileField(upload_to="store")

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='category')
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
    
class AppSection(models.Model):
    category = models.ForeignKey(Category, related_name= "section", on_delete=models.CASCADE) 
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='app_section')
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    


class AppTemplate(models.Model):
    section = models.ForeignKey(AppSection, related_name= 'app_template',on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="app_template")
    active = models.BooleanField(default=False)
    components = models.JSONField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    

class StorTemplates(models.Model):
    store = models.ForeignKey(Store, related_name='user_templates', on_delete=models.CASCADE)
    app_section = models.ForeignKey(AppSection, related_name='user_templates', on_delete=models.CASCADE)
    app_templates = models.ForeignKey(AppTemplate, related_name='user_templates', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    components = models.JSONField()
    components_backup = models.JSONField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.order
    