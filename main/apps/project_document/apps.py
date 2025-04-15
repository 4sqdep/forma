from django.apps import AppConfig


class ProjectDocumentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main.apps.project_document'

    def ready(self):
        import main.apps.project_document.signals