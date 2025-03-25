import shutil
import tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from organization.models import Organization

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class OrganizationPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            email='ivan@email.ru',
            first_name='Ivan',
            middle_name='Ivanovich',
            last_name='Ivanov',
            letter_of_attorney='Attorney',
            post='employee',
        )
        cls.organization = Organization.objects.create(
            full_name = 'Limited Liability Company "Company"',
            short_name = 'LLC "Company"',
            address = '000000, Ivanovsk city',
            phone_number = '+71234567890',
            email = 'llc@email.ru',
            main_state_registration_number = '1234567890111',
            tax_identification_number = '1234567890',
            registration_reason_code = '123456789',
            job_title = 'director',
            person_full_name = 'Ivanov Ivan Ivanovich',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(OrganizationPagesTests.user)

    def test_pages_uses_correct_template(self):
        """The URL uses appropriate template."""
        template_pages_names = {
            reverse('organization:organization_create'): 'organization/organization_create.html',
            reverse('organization:organization_edit', kwargs={'organization_id': f'{self.organization.id}'}): 'organization/organization_create.html',
            reverse('organization:organization_detail'): 'organization/organization_detail.html',
        }
        for reverse_name, template in template_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_organization_create_and_organization_edit_show_correct_context(self):
        """organization_create and organization_edit templates formed with thw right context."""
        template_pages_names = {
            reverse('organization:organization_create'),
            reverse('organization:organization_edit', kwargs={'organization_id': f'{self.organization.id}'}),
        }
        for reverse_name in template_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                form_fields = {
                    'full_name': forms.fields.CharField,
                    'short_name': forms.fields.CharField,
                    'address': forms.fields.CharField,
                    'phone_number': forms.fields.CharField,
                    'email': forms.fields.EmailField,
                    'main_state_registration_number': forms.fields.IntegerField,
                    'tax_identification_number': forms.fields.IntegerField,
                    'registration_reason_code': forms.fields.IntegerField,
                    'job_title': forms.fields.CharField,
                    'person_full_name': forms.fields.CharField,
                }
                for value, excepted in form_fields.items():
                    with self.subTest(value=value):
                        form_field = response.context.get('form').fields.get(value)
                        self.assertIsInstance(form_field, excepted)

    def test_rganization_detail_show_correct_context(self):
        """organization_detail tamplate formed with the right context."""
        response = self.authorized_client.get(reverse('organization:organization_detail'))
        self.assertEqual(response.context.get(
            'organization').full_name, 'Limited Liability Company "Company"')
        self.assertEqual(response.context.get(
            'organization').short_name, 'LLC "Company"')
        self.assertEqual(response.context.get(
            'organization').address, '000000, Ivanovsk city')
        self.assertEqual(response.context.get(
            'organization').phone_number, '+71234567890')
        self.assertEqual(response.context.get(
            'organization').email, 'llc@email.ru')
        self.assertEqual(response.context.get(
            'organization').main_state_registration_number, 1234567890111)
        self.assertEqual(response.context.get(
            'organization').tax_identification_number, 1234567890)
        self.assertEqual(response.context.get(
            'organization').registration_reason_code, 123456789)
        self.assertEqual(response.context.get(
            'organization').job_title, 'director')
        self.assertEqual(response.context.get(
            'organization').person_full_name, 'Ivanov Ivan Ivanovich')
