from django.apps import AppConfig


class ConstructionWorkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main.apps.construction_work'

    def ready(self):
        import main.apps.construction_work.signals
