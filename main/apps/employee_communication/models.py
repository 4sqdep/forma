import os
from django.utils.timezone import now
from django.db import models
from main.apps.account.models.user import User
from main.apps.common.models import BaseModel, BaseMeta
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType




class ProblemStatus(models.TextChoices):
    NEW = "new", "New"
    DONE = "done", "Done"
    IN_CORFIRMATION = "in confirmation", "In confirmation"
    IN_PROGRESS = "in progress", "In progress"
    INCOMPLETE = "incomplete", "Incomplete"
    COMPLETED_LATE = "completed late", "Completed late"


def upload_communication_files(instance, filename):
    ext = os.path.splitext(filename)[1]  
    original_name = os.path.splitext(filename)[0]  
    timestamp = now().strftime("%Y_%m_%d") 
    return f"communication_files/{original_name}_{timestamp}{ext}"


def upload_message_files(instance, filename):
    ext = os.path.splitext(filename)[1]  
    original_name = os.path.splitext(filename)[0]  
    timestamp = now().strftime("%Y_%m_%d") 
    return f"message_files/{original_name}_{timestamp}{ext}"



class EmployeeCommunication(BaseModel):
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='sent_communications'
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to=upload_communication_files, null=True, blank=True)
    employee = models.ManyToManyField(
        User, blank=True, related_name='assigned_communications'
    )
    deadline = models.DateField()
    status = models.CharField(
        max_length=255, null=True, blank=True,
        choices=ProblemStatus.choices, default=ProblemStatus.NEW 
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    section = GenericForeignKey('content_type', 'object_id')
    is_read = models.BooleanField(default=False)
    read_time = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta(BaseMeta):
        db_table = "employee_communication"
        verbose_name = "Employee Communication"
        verbose_name_plural = "Employee Communications"



class FileMessage(BaseModel):
    employee_communication = models.ForeignKey(EmployeeCommunication, on_delete=models.SET_NULL, null=True, blank=True)
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='sent_file_messages'
    )
    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='received_file_messages'
    )
    file = models.FileField(upload_to=upload_message_files, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    read_time = models.DateTimeField(null=True, blank=True)

    class Meta(BaseMeta):
        db_table = "file_message"
        verbose_name = "File Message"
        verbose_name_plural = "File Messages"



class TextMessage(BaseModel):
    employee_communication = models.ForeignKey(EmployeeCommunication, on_delete=models.SET_NULL, null=True, blank=True)
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='sent_text_messages'
    )
    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='received_text_messages'
    )
    text = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    read_time = models.DateTimeField(null=True, blank=True)

    class Meta(BaseMeta):
        db_table = "text_message"
        verbose_name = "Text Message"
        verbose_name_plural = "Text Messages"

