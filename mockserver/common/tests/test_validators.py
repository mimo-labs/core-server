from django.test import TestCase
from django.core.exceptions import ValidationError

from common.validators import validate_json, validate_path


class ValidatorsTestCase(TestCase):
    def test_string_is_not_considered_valid_json(self):
        self.assertRaises(ValidationError, validate_json, "string")

    def test_invalid_url_raises_error(self):
        self.assertRaises(ValidationError, validate_path, "test/url")
