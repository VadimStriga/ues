import tempfile
import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from organization.models import Organization


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class OrganizationCreatForm(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            email = 'ivan@email.ru',
            first_name = 'Ivan',
            middle_name = 'Ivanovich',
            last_name = 'Ivanov',
            letter_of_attorney = 'Attorney',
            post = 'employee',
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
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(OrganizationCreatForm.user)
        self.guest_clietn = Client()
    
    def test_edit_organization(self):
        """A valid form edit organization."""
        organization_count = Organization.objects.count()
        full_name = 'Test_Edit_Company',
        short_name = 'TEC',
        address = '000000, Test city',
        phone_number = '+71234567890',
        email = 'testedit@email.ru',
        main_state_registration_number = '1234567890112',
        tax_identification_number = '1234567891',
        registration_reason_code = '123456790',
        job_title = 'Test_Director',
        person_full_name = 'Test Name',
        reverse_redirect = reverse('organization:organization_detail')
        form_data = {
            'full_name': full_name,
            'short_name': short_name,
            'address': address,
            'phone_number': phone_number,
            'email': email,
            'main_state_registration_number': main_state_registration_number,
            'tax_identification_number': tax_identification_number,
            'registration_reason_code': registration_reason_code,
            'job_title': job_title,
            'person_full_name': person_full_name,
        }
        response = self.authorized_client.post(
            reverse('organization:organization_edit', kwargs={'organization_id': f'{self.organization.id}'}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse_redirect)
        self.assertEqual(Organization.objects.count(), organization_count)
        self.assertTrue(Organization.objects.filter(full_name='Test_Edit_Company').exists())

    def test_do_not_create_organization(self):
        """A valid form do not creates a organization."""
        organization_count = Organization.objects.count()
        full_name = 'Test_Edit_Company',
        short_name = 'TEC',
        address = '000000, Test city',
        phone_number = '+71234567890',
        email = 'testedit@email.ru',
        main_state_registration_number = '1234567890112',
        tax_identification_number = '1234567891',
        registration_reason_code = '123456790',
        job_title = 'Test_Director',
        person_full_name = 'Test Name',
        reverse_redirect = reverse('organization:organization_detail')
        form_data = {
            'full_name': full_name,
            'short_name': short_name,
            'address': address,
            'phone_number': phone_number,
            'email': email,
            'main_state_registration_number': main_state_registration_number,
            'tax_identification_number': tax_identification_number,
            'registration_reason_code': registration_reason_code,
            'job_title': job_title,
            'person_full_name': person_full_name,
        }
        response = self.authorized_client.post(reverse('organization:organization_create'),
                                               data=form_data,
                                               follow=True,)
        self.assertRedirects(response, reverse_redirect)
        self.assertEqual(Organization.objects.count(), organization_count)
        self.assertTrue(Organization.objects.filter(full_name='Test_Edit_Company').exists())

    def test_edit_for_nonauthorized_user(self):
        """Thr editing page are not accessible to unauthorized user."""
        reverse_name = reverse('organization:organization_edit', kwargs={'organization_id': f'{self.organization.id}'})
        organization_count = Organization.objects.count()
        full_name = 'Test_Edit_Company',
        short_name = 'TEC',
        address = '000000, Test city',
        phone_number = '+71234567890',
        email = 'testedit@email.ru',
        main_state_registration_number = '1234567890112',
        tax_identification_number = '1234567891',
        registration_reason_code = '123456790',
        job_title = 'Test_Director',
        person_full_name = 'Test Name',
        form_data = {
            'full_name': full_name,
            'short_name': short_name,
            'address': address,
            'phone_number': phone_number,
            'email': email,
            'main_state_registration_number': main_state_registration_number,
            'tax_identification_number': tax_identification_number,
            'registration_reason_code': registration_reason_code,
            'job_title': job_title,
            'person_full_name': person_full_name,
        }
        response = self.guest_clietn.post(reverse_name,
                                          data=form_data,
                                          follow=True,)
        self.assertEqual(Organization.objects.count(), organization_count)
        self.assertFalse(Organization.objects.filter(person_full_name='Test_Director'))
        self.assertRedirects(response, f'/auth/login/?next=/organization_detail/{self.organization.id}/edit/')
