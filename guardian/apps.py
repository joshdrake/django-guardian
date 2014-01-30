from django.apps import AppConfig
from guardian.compat import setup_prototype_methods


class GuardianConfig(AppConfig):
    name = 'guardian'

    def ready(self):
        setup_prototype_methods(self)
