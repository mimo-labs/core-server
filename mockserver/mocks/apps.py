from django.apps import AppConfig


class MocksConfig(AppConfig):
    name = 'mocks'

    def ready(self):
        from mocks import signals  # noqa
