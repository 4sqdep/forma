from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DashboardSubCategoryButton, ProjectDocumentation, NextStageDocuments
from django.contrib.auth.models import User

@receiver(post_save, sender=DashboardSubCategoryButton)
def create_project_documentation(sender, instance, created, **kwargs):
    """DashboardSubCategoryButton yaratilganda 3 ta ProjectDocumentation qo'shish"""
    if created:  # Faqat yangi ma'lumot qo'shilganda ishlaydi
        names = ["Qurilish ishlari", "Montaj ishlari", "Uskunalar"]  # 3 ta hujjat nomi
        for name in names:
            ProjectDocumentation.objects.create(
                subcategories_btn=instance,  # Bog'laymiz
                user=instance.user,  # Foydalanuvchi
                name=name,  # Hujjat nomi
            )


