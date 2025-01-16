from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

from main.apps.dashboard.models.dashboard import DashboardSubCategoryButton
from main.apps.dashboard.models.document import ProjectDocumentation

logger = logging.getLogger(__name__)


@receiver(post_save, sender=DashboardSubCategoryButton)
def create_project_documentation(sender, instance, created, **kwargs):
    """DashboardSubCategoryButton yaratilganda 3 ta ProjectDocumentation qo'shish"""
    if created:  # Faqat yangi ma'lumot qo'shilganda ishlaydi
        names = ["Obyekt pasporti", "Loyiha hujjatlari", "Qurilish montaj ishlari hujjatlari", "Uskunalar hujjatlari"]  # 3 ta hujjat nomi
        for name in names:
            is_obj_password = True if name == "Obyekt pasporti" else False
            is_project_doc = True if name == "Loyiha hujjatlari" else False
            is_work_smr = True if name == "Qurilish montaj ishlari hujjatlari" else False
            is_equipment = True if name == "Uskunalar hujjatlari" else False
            ProjectDocumentation.objects.create(
                subcategories_btn=instance,  # Bog'laymiz
                user=instance.user,  # Foydalanuvchi
                name=name,  # Hujjat nomi
                is_obj_password=is_obj_password, #Obyekt pasporti
                is_project_doc=is_project_doc, #Loyiha hujjatlari
                is_work_smr=is_work_smr,  #Quriish montaj ishlari
                is_equipment=is_equipment, #Uskunalar hujjatlari
            )
