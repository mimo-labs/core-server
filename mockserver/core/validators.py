import json
import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


PATH_REGEX = re.compile(r"^/.*[/]*$")


def validate_json(value):
    try:
        json.loads(value)
    except ValueError:
        raise ValidationError(
            _(f"{value} is not a valid JSON value!")
        )


def validate_path(value):
    if not PATH_REGEX.match(value):
        raise ValidationError(
            _(f"{value} is not a valid URL path!")
        )
