from django.apps import AppConfig

class HealthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'healthapp'

    def ready(self):
        import healthapp.signals  # Import the signals module
