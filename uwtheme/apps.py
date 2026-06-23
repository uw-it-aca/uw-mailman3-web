from django.apps import AppConfig


class UwthemeConfig(AppConfig):
    name = 'uwtheme'

    def ready(self):
        """
        Monkey patch classes and functions to accommodate
        UW multicore Mailman 3 architecture.
        PRO TIP: make sure uwtheme is listed before
        django_mailman3, hyperkitty, or postorius in
        settings.py INSTALLED_APPS.
        """
        try:
            from uwtheme.monkeypatch import monkey_patch

            monkey_patch()
        except ImportError:
            pass
