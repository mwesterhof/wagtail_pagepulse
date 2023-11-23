from django.apps import AppConfig


class PagepulseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pagepulse'

    def ready(self):
        from . import signals  # noqa
