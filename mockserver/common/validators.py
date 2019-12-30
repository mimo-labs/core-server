import json
import logging
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)


PATH_REGEX = re.compile(r"^/.*/?$")


def validate_json(value):
    try:
        json.loads(value)
    except (ValueError, TypeError):
        logger.info(f'invalid json {value}')
        raise ValidationError(
            _(f"{value} is not a valid JSON value!")
        )


def validate_path(value):
    if not PATH_REGEX.match(value):
        logger.info(f'invalid path {value}')
        raise ValidationError(
            _(f"{value} is not a valid URL path!")
        )
