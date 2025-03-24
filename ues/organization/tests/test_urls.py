from http import HTTPStatus

from django.test import Client, TestCase


class StaticPagesURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        """Checking the availability of the address /."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_url_uses_correct_template(self):
        """Chekink the template for the adress /."""
        response = self.guest_client.get('/')
        self.assertTemplateUsed(response, 'organization/about_organization.html')
