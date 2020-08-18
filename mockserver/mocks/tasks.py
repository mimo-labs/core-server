import logging
import time

from celery.task import task
from django.conf import settings

from mocks.models import Mock
from mocks.services import EndpointService


logger = logging.getLogger(__name__)


@task(serializer="pickle")
def delete_empty_endpoint(mock: Mock):
    # Defensive guard
    if not mock:
        return

    logger.info("begin clear check endpoint %s" % mock.path)
    if settings.DEBUG:
        start = time.time()

    EndpointService.cleanup_endpoint(mock.path)

    logger.info("finished clear check endpoint")

    if settings.DEBUG:
        end = time.time()
        logger.debug("execution time: %s" % (end - start))
