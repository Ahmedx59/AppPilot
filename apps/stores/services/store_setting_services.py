import json
from django.core.files.base import ContentFile
from django.utils import timezone
# from rest_framework.serializers import ValidationError
from django.core.exceptions import ValidationError


from apps.stores.models import AppSection
from apps.stores.models import Store

class ApplySetting:
    @classmethod
    def process_sections(cls, queryset):
        sections_data = {
            "sections": []
        }

        sections = AppSection.objects.all()
        for section in sections:
            section_dict = {
                "name": section.name,
                "order": section.order,
                "templates": cls.process_templates(queryset, section),
            }
            sections_data["sections"].append(section_dict)


        return sections_data

    @staticmethod
    def process_templates(queryset, section):
        templates_data = []

        templates = section.store_templates.filter(store__in=queryset)
        for template in templates:
            template_dict = {
                "name": f"{section.name}_template_{template.order}",
                "is_active": template.is_active,
                "order": template.order,
                "components": template.components,
                # "components": ApplySetting.process_components(template),
            }
            templates_data.append(template_dict)

        return templates_data

    @staticmethod
    def process_components(template):
        components_data = []

        for comp in template.components:
            components_data.append(comp)  

        return components_data

    @classmethod
    def save_setting_file(cls,queryset):

        for store in queryset:
            if store.setting_has_changes == False:
                raise ValidationError(f"store {store.name} has no changes")
            
            data = cls.process_sections([store])

            json_data = json.dumps(data, indent=4)

            file_name = f"store_{store.id}_settings.json"
            store.setting_file.save(file_name, ContentFile(json_data.encode()), save=False)

            store.setting_has_value = True
            store.setting_has_changes = False
            store.save()