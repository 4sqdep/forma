from django.db.models.signals import post_save
from django.dispatch import receiver
from main.apps.object_passport.models.object import Object
from main.apps.project_document.models.project_document_type import ProjectDocumentType


@receiver(post_save, sender=Object)
def create_default_document_types(sender, instance, created, **kwargs):
    if created:
        default_docs = [
            {"name": "Birlamchi hujjatlar", "is_forma": False, "is_section": False, "is_file": True},
            {"name": "Loyiha-smeta hujjatlari", "is_forma": False, "is_section": True, "is_file": False},
            {"name": "Yig'ma jadvat", "is_forma": True, "is_section": False, "is_file": False},
            {"name": "Kerakli ma'lumotlar", "is_forma": False, "is_section": True, "is_file": False}
        ]

        for doc in default_docs:
            ProjectDocumentType.objects.create(
                object=instance,
                name=doc['name'],
                is_forma = doc["is_forma"],
                is_section = doc["is_section"],
                is_file = doc["is_file"]
            )