from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DashboardSubCategoryButton, ProjectDocumentation, NextStageDocuments
from account.models import User


@receiver(post_save, sender=DashboardSubCategoryButton)
def create_project_documentation(sender, instance, created, **kwargs):
    """DashboardSubCategoryButton yaratilganda ProjectDocumentation va NextStageDocuments qo'shish"""
    if created:  # Faqat yangi ma'lumot qo'shilganda ishlaydi
        # 3 ta ProjectDocumentation nomini yaratamiz
        project_documents = {
            "Loyiha hujjatlari": ["Erkin", "Abror", "Rustam"],  # Loyiha hujjatlari uchun foydalanuvchilar
            "Qurilish montaj ishlari": ["Sardor", "Ilhom"],  # Qurilish montaj ishlari uchun foydalanuvchilar
            "Uskunalar": ["Dilshod", "Otabek", "Jasur"]  # Uskunalar uchun foydalanuvchilar
        }

        # Har bir ProjectDocumentation uchun NextStageDocuments yaratamiz
        for doc_name, users in project_documents.items():
            # ProjectDocumentation yaratish
            project_doc = ProjectDocumentation.objects.create(
                subcategories_btn=instance,  # DashboardSubCategoryButton ga bog'lash
                user=instance.user,  # Foydalanuvchi
                name=doc_name,  # Hujjat nomi
            )

            # NextStageDocuments uchun foydalanuvchilarni qo'shish
            for user_name in users:
                try:
                    user = User.objects.get(username=user_name)  # Foydalanuvchini olish
                except User.DoesNotExist:
                    continue  # Agar foydalanuvchi topilmasa, davom etish

                # NextStageDocuments yaratish
                NextStageDocuments.objects.create(
                    project_document=project_doc,  # ProjectDocumentation ga bog'lash
                    subcategories_btn=instance,  # DashboardSubCategoryButton ga bog'lash
                    user=user,  # Foydalanuvchi
                    name=f"{user_name} hujjati",  # Hujjat nomi (foydalanuvchi nomi bilan)
                )