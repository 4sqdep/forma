# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from dashboard.models import ProjectDocumentation, NextStageDocuments
#
#
#
#
# @receiver(post_save, sender=ProjectDocumentation)
# def create_next_stage_documents(sender, instance, created, **kwargs):
#     """ProjectDocumentation name harbirini tekshirib har biriga alohida alohida malumot post qilish"""
#     if created and not getattr(instance, 'skip_signal', False):
#         if instance.name == "Loyiha hujjatlar":
#             print("WWWWWW", instance.name)
#             next_stage_data = ["Malumot1", "Malumot2", "Malumot3"]
#             for data in next_stage_data:
#                 NextStageDocuments.objects.create(
#                     project_document=instance,  # ProjectDocumentation bilan bog'lash
#                     subcategories_btn=instance.subcategories_btn,  # Bog'langan subcategories_btn
#                     user=instance.user,  # Foydalanuvchi
#                     name=data,  # Dinamik nom yaratish
#                 )