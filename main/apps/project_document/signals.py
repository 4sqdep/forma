from django.db.models.signals import post_save
from django.dispatch import receiver
from main.apps.object_passport.models.object import Object
from main.apps.project_document.models.project_document_type import ProjectDocumentType
from main.apps.project_document.models.project_file import ProjectDocumentFile




@receiver(post_save, sender=Object)
def create_default_document_types(sender, instance, created, **kwargs):
    if created:
        default_docs = [
            {"name": "Birlamchi hujjatlar", "is_forma": False, "is_section": False, "is_file": True},
            {"name": "Loyiha-smeta hujjatlari", "is_forma": False, "is_section": True, "is_file": False},
            {"name": "Yig'ma jadval", "is_forma": True, "is_section": False, "is_file": False},
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


@receiver(post_save, sender=ProjectDocumentType)
def create_default_file_name(sender, instance, created, **kwargs):
    if created and instance.name == "Birlamchi hujjatlar":
        default_name = [
            'Loyihani ishlab chiqish uchun asos hujjat (PQ, VMQ, PF)',
            "Oʻzbekgidroenergo AJ yigʻilish bayoni",
            'TZ ishlab chiqish RD uchun',
            'TD tayyorlash (loyihachi aniqlash uchun)',
            'TD Markaz xulosa olish (loyihachi aniqlash uchun)',
            "Tender (Tanlov) oʻtkazish RD",
            "Shartnoma RD",
            "Prezentatsiya tayyorlash",
            "Shartnoma RD (Markaz) xulosasini olish",
            "Planshet tayyorlash",
            "Qizil chiziq olish",
            "Atrof muhitga ta’sirni baholash (ZVOS) ishlab chiqish",
            "(ZVOS) xulosa olish",
            "Kompensatsiya toʻlovlarini qilish",
            "Hokim qarori yer ajratish",
            "Arxitektura rejalashtirish topshirigʻi (APZ)",
            "Shaharsozlik kengashi yigʻilish bayoni (Protokol GUAS)",
            "Tex. Usloviya Elektr.energiya",
            "Elektr ta’minoti loyiha hujjatlarini Energiyainspektsiya kelishish",
            "Tex. Proyekt berish loyihachiga",
            "Sogʻlosovaniya Plan trassa (LEP)",
            "Seysmologiya instituti xulosasi",
            "Ekspertiza kiritish (RD)",
            "Ekspertiza xulosasini olish (RD)",
            "TD QMI uchun",
            "Shartnoma (markazga kiritish) QMI",
            "Shartnoma (markazga kiritish) QMI xulosa olish",
            "Ob’ektni roʻyxatdan oʻtkazish",
            "Geologiya",
            "Gidrologiya",
            "Topografiya",
            "Lira model"
        ]

        for name in default_name:
            ProjectDocumentFile.objects.create(
                project_document_type=instance,
                name=name
            )