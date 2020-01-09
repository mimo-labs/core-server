from django.apps import AppConfig


class MocksConfig(AppConfig):
    name = 'authentication'

    def ready(self):
        from authentication import signals  # noqa
