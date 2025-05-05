from django.db.models.signals import post_save
from django.dispatch import receiver
from main.apps.object_passport.models.object import Object
from main.apps.construction_work.models.section import ConstructionInstallationSection



@receiver(post_save, sender=Object)
def create_default_document_types(sender, instance, created, **kwargs):
    if created:
        default_docs = [
            {"title": "Bajarilgan ishlar dalolatnoma F-3 F-2", "is_forma": False, "is_file": True},
            {"title": "Ijro hujjatlari", "is_forma": False, "is_file": True},
            {"title": "Yig'ma jadval", "is_forma": True, "is_file": False},
            {"title": "Kerakli ma'lumotlar", "is_forma": False, "is_file": True}
        ]

        for doc in default_docs:
            ConstructionInstallationSection.objects.create(
                object=instance,
                title=doc['title'],
                is_forma = doc["is_forma"],
                is_file = doc["is_file"]
            )