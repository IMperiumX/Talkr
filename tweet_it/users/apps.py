from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "tweet_it.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import tweet_it.users.signals  # noqa F401
        except ImportError:
            pass
