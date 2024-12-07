from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DashboardSubCategoryButton, ProjectDocumentation, NextStageDocuments
from account.models import User


@receiver(post_save, sender=DashboardSubCategoryButton)
def create_project_documentations(instance):
    """ProjectDocumentation uchun ma'lumotlarni qo'shish"""
    document_names = ["Loyiha hujjatlari", "Qurilish montaj ishlari", "Uskunalar"]
    project_docs = []
    for name in document_names:
        project_doc = ProjectDocumentation.objects.create(
            subcategories_btn=instance,  # DashboardSubCategoryButton bilan bog'lash
            user=instance.user,  # Foydalanuvchi
            name=name,  # Hujjat nomi
        )
        project_docs.append(project_doc)  # Keyingi bosqichda foydalanish uchun saqlaymiz
    return project_docs


# 2. NextStageDocuments yaratish uchun funksiya
def create_next_stage_documents(project_doc, instance):
    """NextStageDocuments uchun ma'lumotlarni qo'shish"""
    # Hujjat nomlari bo'yicha foydalanuvchi ismlarini aniqlash
    user_names_by_document = {
        "Loyiha hujjatlari": ["Erkin", "Abror", "Rustam"],
        "Qurilish montaj ishlari": ["Sardor", "Ilhom"],
        "Uskunalar": ["Dilshod", "Otabek", "Jasur"],
    }

    # Hujjat nomiga qarab foydalanuvchi ismlarini topamiz
    user_names = user_names_by_document.get(project_doc.name, [])
    for user_name in user_names:
        try:
            user = User.objects.get(username=user_name)  # Foydalanuvchini topamiz
        except User.DoesNotExist:
            print(f"Foydalanuvchi topilmadi: {user_name}")  # Debug uchun log yozish
            continue  # Agar foydalanuvchi topilmasa, keyingisiga o'tamiz

        # NextStageDocuments ma'lumotini yaratamiz
        NextStageDocuments.objects.create(
            project_document=project_doc,  # ProjectDocumentation bilan bog'lash
            subcategories_btn=instance,  # DashboardSubCategoryButton bilan bog'lash
            user=user,  # Foydalanuvchi
            name=f"{project_doc.name} - {user_name}",  # Hujjat nomiga foydalanuvchi nomini qo'shish
        )


# 3. Signal - asosiy mantiq
@receiver(post_save, sender=DashboardSubCategoryButton)
def create_project_and_next_stage(sender, instance, created, **kwargs):
    """DashboardSubCategoryButton yaratilganda ProjectDocumentation va NextStageDocuments yaratish"""
    if created:  # Faqat yangi yaratilganda ishlaydi
        # 1. ProjectDocumentation yaratish
        project_docs = create_project_documentations(instance)

        # 2. NextStageDocuments yaratish
        for project_doc in project_docs:
            create_next_stage_documents(project_doc, instance)