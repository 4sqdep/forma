from django.core.management.base import BaseCommand
from main.apps.object_passport.models.object import Object
from main.apps.project_document.models.project_document_type import ProjectDocumentType
from main.apps.project_document.models.project_file import ProjectDocumentFile








ADDITIONAL_DOC_NAMES = [
    "Loyhani ishlab chiqish uchun asos hujjat (PQ, VMQ, PF)",
    "\"O'zbekgidroenergo\" AJ yig'ilish bayoni",
    "TZ ishlab chiqish RD uchun",
    "TD tayyorlash (loyihachi aniqlash uchun)",
    "TD Markaz xulosa olish (loyihachi aniqlash uchun)",
    "Tender (Tanlov) o'tkazish RD",
    "Shartnoma RD",
    "Prezintatsiya tayyorlash",
    "Shartnoma RD (Markaz) xulosasini olish",
    "Planshet tayyorlash",
    "Qizil chizishni olish",
    "Atrof muhitga ta’sirni baholash (ZVOS) ishlab chiqish",
    "(ZVOS) xulosa olish",
    "Kompensatsiya to‘lovlarini qilish",
    "Hokim qarori yer ajratish",
    "Arxitektura rejalashtirish topshirig‘i (APZ)",
    "Shaharsizlik kengashi yig‘ilish bayoni (Protokol GUAS)",
    "Tex. Uslova Elektr.energiya",
    "Elektr ta’minoti loyiha hujjatlarini \"Energiyainspektsiya\" kelishish",
    "Tex. Proyekt berish loyihachiga",
    "Sog‘losavaniya Plan trassa (LEP)",
    "Seysmologiya instituti xulosasi",
    "Ekspertiza kiritish (RD)",
    "Ekspertiza xulosasini olish (RD)",
    "TD QMI uchun",
    "Shartnoma (markazga kiritish) QMI",
    "Shartnoma (markazga kiritish) QMI xulosa olish",
    "Obyektni ro‘yxatdan o‘tkazish",
    "Geologiya",
    "Gidrologiya",
    "Topografiya",
    "Lira model",
]




class Command(BaseCommand):
    help = "Create additional ProjectDocumentFile records if 'Birlamchi hujjatlar' exists"

    def handle(self, *args, **kwargs):
        for obj in Object.objects.all():
            try:
                doc_type = ProjectDocumentType.objects.get(object=obj, name="Birlamchi hujjatlar")
            except ProjectDocumentType.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Skipped object {obj.id}: no 'Birlamchi hujjatlar' found."))
                continue

            for name in ADDITIONAL_DOC_NAMES:
                doc_file, created = ProjectDocumentFile.objects.get_or_create(
                    name=name,
                    project_document_type=doc_type,
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created: {name} for object {obj.id}"))
                else:
                    self.stdout.write(self.style.NOTICE(f"Already exists: {name} for object {obj.id}"))
