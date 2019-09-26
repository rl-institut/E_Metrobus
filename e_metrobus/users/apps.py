from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "e_metrobus.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import e_metrobus.users.signals  # noqa F401
        except ImportError:
            pass
