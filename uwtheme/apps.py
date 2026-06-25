from django.apps import AppConfig
import logging


logger = logging.getLogger(__name__)


class UwthemeConfig(AppConfig):
    name = 'uwtheme'

    def ready(self):
        """
        Monkey patch classes and functions to accommodate
        seamless interface to UW multi instance Mailman 3
        architecture.

        PRO TIP: make sure uwtheme is listed before
        django_mailman3, hyperkitty, and postorius in
        settings.py INSTALLED_APPS.
        """
        try:
            from uwtheme.monkeypatch import monkey_patch

            monkey_patch()
        except ImportError as ex:
            logger.error(f"MONKEY PATCH ERROR {ex}")
            pass
