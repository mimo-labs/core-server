import logging
import time

from celery.task import task
from django.conf import settings

from mocks.services import EndpointService


logger = logging.getLogger(__name__)


@task()
def delete_empty_endpoint(path_name: str, project_id: int):
    logger.info("begin clear check endpoint %s" % path_name)
    if settings.DEBUG:
        start = time.time()

    path = EndpointService.get_endpoint_by_name_and_project(path_name, project_id)
    EndpointService.cleanup_endpoint(path)

    logger.info("finished clear check endpoint")

    if settings.DEBUG:
        end = time.time()
        logger.debug("execution time: %s" % (end - start))
