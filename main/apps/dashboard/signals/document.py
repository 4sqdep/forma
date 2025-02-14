from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

from main.apps.dashboard.models.dashboard import Object
from main.apps.dashboard.models.document import ProjectDocumentation

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Object)
def create_project_documentation(sender, instance, created, **kwargs):
    if created:  
        names = ["Obyekt pasporti", "Loyiha hujjatlari", "Qurilish montaj ishlari hujjatlari", "Uskunalar hujjatlari"] 
        for name in names:
            is_obj_password = True if name == "Obyekt pasporti" else False
            is_project_doc = True if name == "Loyiha hujjatlari" else False
            is_work_smr = True if name == "Qurilish montaj ishlari hujjatlari" else False
            is_equipment = True if name == "Uskunalar hujjatlari" else False
            ProjectDocumentation.objects.create(
                subcategories_btn=instance,  
                created_by=instance.created_by, 
                name=name,  
                is_obj_password=is_obj_password, 
                is_project_doc=is_project_doc, 
                is_work_smr=is_work_smr,  
                is_equipment=is_equipment, 
            )
