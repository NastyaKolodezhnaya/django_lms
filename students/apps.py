from django.apps import AppConfig


class StudentsConfig(AppConfig):
    name = 'students'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import students.signals
