from django.db import models
from main.apps.account.models.user import User
from main.apps.common.models import BaseModel, BaseMeta
import os
from django.utils.timezone import now


class ProblemStatus(models.TextChoices):
    NEW = "new", "New"
    DONE = "done", "Done",
    IN_CORFIRMATION = "in confirmation", "In confirmation"
    IN_PROGRESS = "in progress", "In progress"
    INCOMPLETE = "incomplete", "Incomplete"



def upload_problem_files(instance, filename):
    ext = os.path.splitext(filename)[1]  
    original_name = os.path.splitext(filename)[0]  
    timestamp = now().strftime("%Y_%m_%d") 
    return f"problem_files/{original_name}_{timestamp}{ext}"



class EmployeeCommunication(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to=upload_problem_files, null=True, blank=True)
    employee = models.ManyToManyField(User, null=True, blank=True)
    deadline = models.DateField()
    status = models.CharField(max_length=255, null=True, blank=True, choices=ProblemStatus.NEW)


    def __str__(self):
        return self.title

    class Meta(BaseMeta):
        db_table = "employee_communication"
        verbose_name = "Employee Communication"
        verbose_name_plural = "Employee Communications"

