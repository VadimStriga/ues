from http import HTTPStatus
import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from counterparties.models import (Comment,
                                   Contract,
                                   Counterparty,
                                   Document as Counterparties_Document)
from electricity_accounting.models import (Calculation,
                                           CurrentTransformer,
                                           Document,
                                           ElectricityMeter,
                                           ElectricityMeteringPoint,
                                           Tariff,
                                           InterconnectedPoints)


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
TEST_CACHE_SETTING = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

User = get_user_model()


@override_settings(CACHES=TEST_CACHE_SETTING, MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ElectricityAccountingCreateForm(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif',
        )
        cls.user = User.objects.create(
            email = 'ivan@email.ru',
            first_name = 'Ivan',
            middle_name = 'Ivanovich',
            last_name = 'Ivanov',
            letter_of_attorney = 'Attorney',
            post = 'employee',
        )
        cls.counterparty = Counterparty.objects.create(
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
        cls.contract = Contract.objects.create(
            counterparty = cls.counterparty,
            title = '123',
            conclusion_date = '2001-01-01',
            contract_price = '123',
            purchase_code = '1234567890',
            description = 'Hard work',
            сompletion_date = '2001-01-01',
            actual_cost = '123',
        )
        cls.contract_document = Counterparties_Document.objects.create(
            contract = cls.contract,
            conclusion_date = '2001-01-01',
            title = 'Contract Document Title',
            file = uploaded,
        )
        cls.contract_comment = Comment.objects.create(
            author = cls.user,
            text = 'Long contract comment for testing',
            created = '2001-01-01',
            updated = '2001-01-01',
            content_type = ContentType.objects.get_for_model(Contract),
            object_id = cls.contract.id,
        )
        cls.point = ElectricityMeteringPoint.objects.create(
            constant_losses = 0,
            contract = cls.contract,
            name = 'electricity_metering_point',
            location = 'location',
            losses = 0,
            margin = 0,
            power_supply = 'power_supply',
            tariff = 'tariff-free',
            transformation_coefficient = 1,
            type_of_accounting = 'Calculation accounting',
        )
        cls.point_comment = Comment.objects.create(
            author = cls.user,
            text = 'Long point comment for testing',
            created = '2001-01-01',
            updated = '2001-01-01',
            content_type = ContentType.objects.get_for_model(ElectricityMeteringPoint),
            object_id = cls.point.id,
        )
        cls.point_document = Document.objects.create(
            point = cls.point,
            conclusion_date = '2001-01-01',
            title = 'Point Document Title',
            file = uploaded
        )
        cls.meter = ElectricityMeter.objects.create(
            is_active = True,
            mark = 'Mercury',
            number = '1234567890',
            installation_date = '2001-01-01',
            date_of_next_verification = '2033-01-01',
            point = cls.point,
            photo = uploaded,
        )
        cls.transformer = CurrentTransformer.objects.create(
            is_active = True,
            mark = 'TT-0,66',
            number = '1234567890',
            installation_date = '2001-01-01',
            date_of_next_verification = '2033-01-01',
            point = cls.point,
            photo = uploaded,
        )
        cls.tariff = Tariff.objects.create(
            pub_date = '2001-01-01',
            begin_tariff_period = '2001-01-01',
            end_tariff_period = '2001-01-31',
            urban_tariff_1 = 3.5,
            urban_tariff_2 = 4.0,
            urban_tariff_3 = 5.0,
            rural_tariff_1 = 2.5,
            rural_tariff_2 = 3.6,
            rural_tariff_3 = 4.2,
            high_voltage_tariff = 5.1,
            medium_voltage_tariff_1 = 5.5,
            medium_voltage_tariff_2 = 5.8,
            low_voltage_tariff = 7.0,
        )
        cls.calculation = Calculation.objects.create(
            point = cls.point,
            meter = cls.meter,
            entry_date = '2001-01-01',
            readings = 12345.67,
            previous_entry_date = '2001-01-01',
            previous_readings = 12300.67,
            difference_readings = 45.0,
            transformation_coefficient = 1,
            amount = 45.0,
            deductible_amount = 0,
            losses = 10,
            constant_losses = 1,
            result_amount = 39.5,
            tariff1 = 7.0,
            tariff2 = 7.0,
            tariff3 = 7.0,
            margin = 1,
            accrued = 316.0,
            accrued_NDS = 379.2,
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
    
    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(ElectricityAccountingCreateForm.user)
        self.author_client = Client()
        self.author_client.force_login(
            ElectricityAccountingCreateForm.contract_comment.author)
        self.guest_client = Client()

    def test_create_and_edit_point(self):
        """A valid form creates and edits a electricity metering point."""
        point_count = ElectricityMeteringPoint.objects.count()
        templates_pages_names = [
            reverse('accounting:point_create', kwargs={'contract_id': f'{self.contract.id}'}),
            reverse('accounting:point_edit', kwargs={'point_id': f'{self.point.id}'}),
        ]

        location = 'location'
        power_supply = 'power_supply'
        type_of_accounting = 'Calculation accounting'
        tariff = 'tariff-free'
        margin = 0
        losses = 0
        constant_losses = 0
        transformation_coefficient = 1
        
        for reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                if reverse_name == reverse('accounting:point_create', kwargs={'contract_id': f'{self.contract.id}'}):
                    name = 'new_electricity_metering_point_name'
                    reverse_redirect = reverse('counterparties:contract_detail', kwargs={'contract_id': f'{self.contract.id}'})
                    point_count += 1
                else:
                    name = 'edit_electricity_metering_point_name'
                    reverse_redirect = reverse('accounting:point_detail', kwargs={'point_id': f'{self.point.id}'})
                form_data = {
                    'name': name,
                    'location': location,
                    'power_supply': power_supply,
                    'type_of_accounting': type_of_accounting,
                    'tariff': tariff,
                    'margin': margin,
                    'losses': losses,
                    'constant_losses': constant_losses,
                    'transformation_coefficient': transformation_coefficient, 
                }
                response = self.authorized_client.post(reverse_name,
                                                       data=form_data,
                                                       follow=True,)
                self.assertRedirects(response, reverse_redirect)
                self.assertEqual(ElectricityMeteringPoint.objects.count(), point_count)
                if reverse_name == reverse('accounting:point_create', kwargs={'contract_id': f'{self.contract.id}'}):
                    self.assertTrue(ElectricityMeteringPoint.objects.filter(name='new_electricity_metering_point_name').exists())
                else:
                    self.assertTrue(ElectricityMeteringPoint.objects.filter(name='edit_electricity_metering_point_name').exists())
