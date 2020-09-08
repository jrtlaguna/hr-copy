from django.apps import AppConfig


class LeavesConfig(AppConfig):
    name = 'leaves'

    def ready(self):
        from leaves import signals