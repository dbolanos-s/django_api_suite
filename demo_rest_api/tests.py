from django.test import SimpleTestCase
from django.urls import reverse


class DemoRestApiTests(SimpleTestCase):
    def test_demo_api_collection(self):
        response = self.client.get(reverse("demo_rest_api"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_demo_api_requires_name_and_email(self):
        response = self.client.post(
            reverse("demo_rest_api"),
            {"name": "SinCorreo"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
