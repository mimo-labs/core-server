import logging

from django.test.runner import DiscoverRunner


class LoggingDisabledTestRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        logging.disable(logging.CRITICAL)

        return super(LoggingDisabledTestRunner, self).run_tests(test_labels, extra_tests, **kwargs)
