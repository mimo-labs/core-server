from django.test import TestCase, Client


class ViewsTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def test_unexistent_mock_returns_404(self):
        response = self.c.get('/mock/that/does/not/exist')
        self.assertEqual(response.status_code, 404)
