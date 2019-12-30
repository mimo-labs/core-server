from django.apps import AppConfig


class MocksConfig(AppConfig):
    name = 'mocks'

    def ready(self):
        import mocks.signals  # noqa
