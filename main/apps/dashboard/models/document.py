from django.db import models
from main.apps.dashboard.models.dashboard import Object
from main.apps.common.models import BaseModel, BaseMeta




class ProjectDocumentation(BaseModel):
    subcategories_btn = models.ForeignKey(Object, on_delete=models.SET_NULL,
                                          verbose_name="Loyiha nomi", blank=True,
                                          null=True, related_name="projectdocumentation")
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")
    is_obj_password = models.BooleanField(default=False, verbose_name="Obyekt pasporti?")
    is_project_doc = models.BooleanField(default=False, verbose_name="Loyiha hujjatlari?")
    is_work_smr = models.BooleanField(default=False, verbose_name="Qurilish montaj ishlari hujjatlari?")
    is_equipment = models.BooleanField(default=False, verbose_name="Uskunalar hujjatlari?")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    def __str__(self):
        return f"{self.subcategories_btn} -- {self.name}"

    class Meta(BaseMeta):
        db_table = "project_documentation"
        verbose_name = "Project Documentation"
        verbose_name_plural = "Project Documentations"



class NextStageDocuments(BaseModel):
    object = models.ForeignKey(Object, on_delete=models.SET_NULL,
                                          verbose_name="Loyiha nomi", blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")
    is_forma = models.BooleanField(default=False, verbose_name="Forma")
    is_section = models.BooleanField(default=False, verbose_name="Bo'lim")
    is_file = models.BooleanField(default=False, verbose_name="Fayl yuklash")

    def __str__(self):
        return f"{self.name}"

    class Meta(BaseMeta):
        db_table = "next_stage_documents"
        verbose_name = "Next Stage Document"
        verbose_name_plural = "Next Stage Documents"



class ProjectSections(BaseModel):
    next_stage_documents = models.ForeignKey(NextStageDocuments, on_delete=models.SET_NULL,
                                             verbose_name="Keyingi hujjat", blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")

    def __str__(self):
        return f"{self.next_stage_documents} -- {self.name}"
    
    class Meta(BaseMeta):
        db_table = "project_sections"
        verbose_name = "Project Section"
        verbose_name_plural = "Project Sections"



class DocumentFiles(BaseModel):
    document = models.ForeignKey(NextStageDocuments, on_delete=models.SET_NULL, verbose_name="Next Stage Document", blank=True, null=True)
    project_section = models.ForeignKey(ProjectSections, on_delete=models.SET_NULL, verbose_name="Project Section", blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    calendar = models.DateField(blank=True, null=True)
    file_code = models.CharField(max_length=20, blank=True, null=True, )
    files = models.FileField(upload_to="document_files/", blank=True, null=True)

    def __str__(self):
        return f"{self.document} -- {self.name}"

    class Meta(BaseMeta):
        db_table = "document_files"
        verbose_name = "Docuemtn File"
        verbose_name_plural = "Document Files"