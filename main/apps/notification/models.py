from django.db import models
from main.apps.account.models import User
from main.apps.resourceflow.models import ResourceRequest, ResourceReturn, StatusChoices
from ..common.models import BaseModel, BaseMeta
from django.db.models.signals import post_save
from django.dispatch import receiver




class Notification(BaseModel):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="employee_notifications")
    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="manager_notifications")
    resource_request = models.ForeignKey(ResourceRequest, on_delete=models.CASCADE, null=True, blank=True, related_name="notifications")
    message = models.CharField(max_length=255, null=True, blank=True)
    is_read = models.BooleanField(default=False)

    class Meta(BaseMeta):
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications' 




@receiver(post_save, sender=ResourceRequest)
def notify_assistants_on_resource_request_status_change(sender, instance, **kwargs):
    if instance.status in [StatusChoices.REJECTED, StatusChoices.RESOLVED]:
        Notification.objects.create(
            employee=instance.sender,
            manager=instance.receiver,
            resource_request=instance,
            message=f"Resource Request #{instance.id} status has changed to {instance.status}."
        )



@receiver(post_save, sender=ResourceReturn)
def notify_assistants_on_resource_return_status_change(sender, instance, **kwargs):
    if instance.status in [StatusChoices.RESOLVED]:
        Notification.objects.create(
            employee=instance.sender,
            manager=instance.receiver,
            resource_request=instance,
            message=f"Resource Request #{instance.id} status has changed to {instance.status}."
        )
