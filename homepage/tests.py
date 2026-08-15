from django.test import SimpleTestCase
from django.urls import reverse


class HomepageViewsTests(SimpleTestCase):
    def test_homepage_index_renders(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Backend")
        self.assertContains(response, "team.jpg")

    def test_homepage_index_alias(self):
        response = self.client.get("/index/")
        self.assertEqual(response.status_code, 200)
