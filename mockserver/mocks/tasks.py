import logging
import time

from celery.task import task
from django.conf import settings

from mocks.models import Mock, Endpoint


logger = logging.getLogger(__name__)


@task(serializer="pickle")
def delete_empty_endpoint(mock: Mock):
    logger.info("begin clear check endpoint %s" % mock.path)
    if settings.DEBUG:
        start = time.time()

    mock_endpoint: Endpoint = mock.path
    any_endpoint_mocks = mock_endpoint.mocks.all().exists()

    if not any_endpoint_mocks:
        logger.info("detected empty endpoint. deleting")
        mock_endpoint.delete()
    else:
        logger.info("endpoint not empty. skipping")

    logger.info("finished clear check endpoint")

    if settings.DEBUG:
        end = time.time()
        logger.debug("execution time: %s" % (end - start))
