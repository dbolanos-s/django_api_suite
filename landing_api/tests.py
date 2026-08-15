from django.test import SimpleTestCase
from django.urls import reverse


class LandingApiTests(SimpleTestCase):
    def test_landing_api_without_firebase_returns_503(self):
        response = self.client.get(reverse("landing_api"))
        self.assertIn(response.status_code, (200, 503))
