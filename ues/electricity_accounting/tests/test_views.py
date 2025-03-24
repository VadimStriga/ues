import shutil
import tempfile

from django import forms
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
from electricity_accounting.views import NUMBER_OF_OUTPUT_POINTS


NUMBER_OF_TEST_POINTS = NUMBER_OF_OUTPUT_POINTS + 5
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
YEAR = '2001'

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ElectricityAccountingPagesTests(TestCase):
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
        cls.lower_point = ElectricityMeteringPoint.objects.create(
            constant_losses = 0,
            contract = cls.contract,
            name = 'lower_electricity_metering_point',
            location = 'location',
            losses = 0,
            margin = 0,
            power_supply = 'power_supply',
            tariff = 'tariff-free',
            transformation_coefficient = 1,
            type_of_accounting = 'Calculation accounting',
        )
        cls.interconnerction = InterconnectedPoints.objects.create(
            head_point = cls.point,
            lower_point = cls.lower_point,
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
        self.authorized_client.force_login(ElectricityAccountingPagesTests.user)
        self.author_client = Client()
        self.author_client.force_login(ElectricityAccountingPagesTests.contract_comment.author)
        self.guest_client = Client()

    def test_pages_uses_correct_template(self):
        """The URL uses the appropriate template."""
        template_pages_names = {
            reverse('accounting:points_list'): 'accounting/points_list.html',
            reverse('accounting:point_create', kwargs={'contract_id': f'{self.contract.id}'}): 'accounting/point_create.html',
            reverse('accounting:point_edit', kwargs={'point_id': f'{self.point.id}'}): 'accounting/point_create.html',
            reverse('accounting:point_detail', kwargs={'point_id': f'{self.point.id}'}): 'accounting/point_detail.html',
            reverse('accounting:meter_create', kwargs={'point_id': f'{self.point.id}'}): 'accounting/meter_create.html',
            reverse('accounting:meter_edit', kwargs={'point_id': f'{self.point.id}', 'meter_id': f'{self.meter.id}'}): 'accounting/meter_create.html',
            reverse('accounting:transformer_create', kwargs={'point_id': f'{self.point.id}'}): 'accounting/transformer_create.html',
            reverse('accounting:transformer_edit', kwargs={'point_id': f'{self.point.id}', 'transformer_id': f'{self.transformer.id}'}): 'accounting/transformer_create.html',
            reverse('accounting:tariffs_list'): 'accounting/tariffs_list.html',
            reverse('accounting:tariff_create'): 'accounting/tariff_create.html',
            reverse('accounting:tariff_edit', kwargs={'tariff_id': f'{self.tariff.id}'}): 'accounting/tariff_create.html',
            reverse('accounting:calculation_edit', kwargs={'point_id': f'{self.point.id}', 'calculation_id': f'{self.calculation.id}'}): 'accounting/calculation_edit.html',
            reverse('accounting:interconnection_create', kwargs={'point_id': f'{self.point.id}'}): 'accounting/interconnection_create.html',
        }
        for revers_name, template in template_pages_names.items():
            with self.subTest(revers_name=revers_name):
                response = self.authorized_client.get(revers_name)
                self.assertTemplateUsed(response, template)

    def test_point_create_point_edit_show_correct_contex(self):
        """point_create and point_edit templates formed with the right context."""
        template_pages_name = (
            reverse('accounting:point_create', kwargs={'contract_id': f'{self.contract.id}'}),
            reverse('accounting:point_edit', kwargs={'point_id': f'{self.point.id}'}),
        )
        for revers_name in template_pages_name:
            with self.subTest(revers_name=revers_name):
                response = self.authorized_client.get(revers_name)
                form_fields = {
                    'name': forms.fields.CharField,
                    'location': forms.fields.CharField,
                    'power_supply': forms.fields.CharField,
                    'type_of_accounting': forms.fields.TypedChoiceField,
                    'tariff': forms.fields.TypedChoiceField,
                    'margin': forms.fields.FloatField,
                    'losses': forms.fields.FloatField,
                    'constant_losses': forms.fields.IntegerField,
                    'transformation_coefficient': forms.fields.IntegerField,
                }
                for value, excepted in form_fields.items():
                    with self.subTest(value=value):
                        form_field = response.context.get('form').fields.get(value)
                        self.assertIsInstance(form_field, excepted)

    def test_point_detail_show_correct_context(self):
        """point_detail template formed with correct context."""
        response = self.authorized_client.get(reverse('accounting:point_detail', kwargs={'point_id': f'{self.point.id}'}))
        self.assertEqual(response.context.get('point').name, 'electricity_metering_point')
        self.assertEqual(response.context.get('point').location, 'location')
        self.assertEqual(response.context.get('point').losses, 0)
        self.assertEqual(response.context.get('point').constant_losses, 0)
        self.assertEqual(response.context.get('point').margin, 0)
        self.assertEqual(response.context.get('point').power_supply, 'power_supply')
        self.assertEqual(response.context.get('point').tariff, 'tariff-free')
        self.assertEqual(response.context.get('point').transformation_coefficient, 1)
        self.assertEqual(response.context.get('point').type_of_accounting, 'Calculation accounting')
        self.assertQuerySetEqual(response.context.get('calculations'), [self.calculation])
        self.assertEqual(response.context.get('calculations').first().entry_date.strftime('%Y-%m-%d'), '2001-01-01')
        self.assertEqual(response.context.get('calculations').first().readings, 12345.67)
        self.assertIsInstance(response.context.get('comment_form').fields.get('text'), forms.fields.CharField)
        self.assertQuerySetEqual(response.context.get('comments'), [self.point_comment])
        self.assertEqual(response.context.get('comments').first().text, 'Long point comment for testing')
        self.assertQuerySetEqual(response.context.get('documents'), [self.point_document])
        self.assertEqual(response.context.get('documents').first().title, 'Point Document Title')
        self.assertEqual(response.context.get('documents').first().conclusion_date.strftime('%Y-%m-%d'), '2001-01-01')
        self.assertEqual(response.context.get('documents_count'), 1)
        self.assertIsInstance(response.context.get('document_form').fields.get('title'), forms.fields.CharField)
        self.assertIsInstance(response.context.get('document_form').fields.get('conclusion_date'), forms.fields.DateField)
        self.assertIsInstance(response.context.get('document_form').fields.get('file'), forms.fields.FileField)
        self.assertEqual(response.context.get('previous_readings'), 12345.67)
        self.assertEqual(response.context.get('is_population'), False)
        self.assertEqual(response.context.get('tariff1'), 0)
        self.assertEqual(response.context.get('tariff2'), 0)
        self.assertEqual(response.context.get('tariff3'), 0)
        self.assertIsInstance(response.context.get('calculation_form').fields.get('entry_date'), forms.fields.DateField)
        self.assertIsInstance(response.context.get('calculation_form').fields.get('readings'), forms.fields.IntegerField)
        self.assertEqual(response.context.get('deductible_amount'), 0)
        self.assertQuerySetEqual(response.context.get('meters'), [self.meter])
        self.assertEqual(response.context.get('meters').first().is_active, True)
        self.assertEqual(response.context.get('meters').first().mark, 'Mercury')
        self.assertEqual(response.context.get('meters').first().number, '1234567890')
        self.assertEqual(response.context.get('meters').first().installation_date.strftime('%Y-%m-%d'), '2001-01-01')
        self.assertEqual(response.context.get('meters').first().date_of_next_verification.strftime('%Y-%m-%d'), '2033-01-01')
        self.assertEqual(response.context.get('meters').first().photo.name, 'contracts/small.gif')
        self.assertEqual(response.context.get('alert_flag'), False)
        self.assertEqual(response.context.get('current_meter_number'), '1234567890')
        self.assertQuerySetEqual(response.context.get('old_meters'), [])
        self.assertQuerySetEqual(response.context.get('transformers'), [self.transformer])
        self.assertEqual(response.context.get('transformers').first().is_active, True)
        self.assertEqual(response.context.get('transformers').first().mark, 'TT-0,66')
        self.assertEqual(response.context.get('transformers').first().number, '1234567890')
        self.assertEqual(response.context.get('transformers').first().installation_date.strftime('%Y-%m-%d'), '2001-01-01')
        self.assertEqual(response.context.get('transformers').first().date_of_next_verification.strftime('%Y-%m-%d'), '2033-01-01')
        self.assertQuerySetEqual(response.context.get('old_transformers'), [])
        self.assertEqual(response.context.get('interconnected_lower_points').first().lower_point.name, 'lower_electricity_metering_point')
        self.assertQuerysetEqual(response.context.get('interconnected_lower_points'), [self.interconnerction])
        self.assertQuerySetEqual(response.context.get('interconnected_head_points'), [])
        

    def test_meter_create_meter_edit_show_correct_contex(self):
        """meter_create and meter_edit templates formed with the right context."""
        template_pages_name = (
            reverse('accounting:meter_create', kwargs={'point_id': f'{self.point.id}'}),
            reverse('accounting:meter_edit', kwargs={'point_id': f'{self.point.id}', 'meter_id': f'{self.meter.id}'}),
        )
        for revers_name in template_pages_name:
            with self.subTest(revers_name=revers_name):
                response = self.authorized_client.get(revers_name)
                form_fields = {
                    'is_active': forms.fields.BooleanField,
                    'mark': forms.fields.CharField,
                    'number': forms.fields.CharField,
                    'installation_date': forms.fields.DateField,
                    'date_of_next_verification': forms.fields.DateField,
                    'photo': forms.fields.ImageField,
                }
                for value, excepted in form_fields.items():
                    with self.subTest(value=value):
                        form_field = response.context.get('form').fields.get(value)
                        self.assertIsInstance(form_field, excepted)

    def test_transformer_create_transformer_edit_show_correct_contex(self):
        """transformer_create and transformer_edit templates formed with the right context."""
        template_pages_name = (
            reverse('accounting:transformer_create', kwargs={'point_id': f'{self.point.id}'}),
            reverse('accounting:transformer_edit', kwargs={'point_id': f'{self.point.id}', 'transformer_id': f'{self.transformer.id}'}),
        )
        for revers_name in template_pages_name:
            with self.subTest(revers_name=revers_name):
                response = self.authorized_client.get(revers_name)
                form_fields = {
                    'is_active': forms.fields.BooleanField,
                    'mark': forms.fields.CharField,
                    'number': forms.fields.CharField,
                    'installation_date': forms.fields.DateField,
                    'date_of_next_verification': forms.fields.DateField,
                    'photo': forms.fields.ImageField,
                }
                for value, excepted in form_fields.items():
                    with self.subTest(value=value):
                        form_field = response.context.get('form').fields.get(value)
                        self.assertIsInstance(form_field, excepted)

    def test_calculation_edit_show_correct_contex(self):
        """calculation_edit templates formed with the right context."""
        reverse_name = reverse('accounting:calculation_edit', kwargs={'point_id': f'{self.point.id}', 'calculation_id': f'{self.calculation.id}'})
        response = self.authorized_client.get(reverse_name)
        form_fields = {
            'entry_date': forms.fields.DateField,
            'readings': forms.fields.IntegerField,
            'previous_entry_date': forms.fields.DateField,
            'previous_readings': forms.fields.IntegerField,
            'difference_readings': forms.fields.IntegerField,
            'transformation_coefficient': forms.fields.IntegerField,
            'amount': forms.fields.IntegerField,
            'deductible_amount': forms.fields.IntegerField,
            'losses': forms.fields.IntegerField,
            'constant_losses': forms.fields.IntegerField,
            'result_amount': forms.fields.IntegerField,
            'tariff1': forms.fields.IntegerField,
            'tariff2':forms.fields.IntegerField,
            'tariff3': forms.fields.IntegerField,
            'margin': forms.fields.IntegerField,
            'accrued': forms.fields.IntegerField,
            'accrued_NDS': forms.fields.IntegerField,
        }
        for value, excepted in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, excepted)

    def test_interconnection_create_show_correct_context(self):
        reverse_name = reverse('accounting:interconnection_create', kwargs={'point_id': f'{self.point.id}'})
        response = self.authorized_client.get(reverse_name)
        self.assertIsInstance(response.context.get('form').fields.get('lower_point'), forms.fields.ChoiceField)

    def test_teriff_create_and_tariff_edit_show_correct_context(self):
        template_pages_names = {
            reverse('accounting:tariff_create'),
            reverse('accounting:tariff_edit', kwargs={'tariff_id': f'{self.tariff.id}'})
        }
        for reverse_name in template_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                form_fields = {
                    'begin_tariff_period': forms.fields.DateField,
                    'end_tariff_period': forms.fields.DateField,
                    'high_voltage_tariff': forms.fields.IntegerField,
                    'medium_voltage_tariff_1': forms.fields.IntegerField,
                    'medium_voltage_tariff_2': forms.fields.IntegerField,
                    'low_voltage_tariff': forms.fields.IntegerField,
                    'urban_tariff_1': forms.fields.IntegerField,
                    'urban_tariff_2': forms.fields.IntegerField,
                    'urban_tariff_3': forms.fields.IntegerField,
                    'rural_tariff_1': forms.fields.IntegerField,
                    'rural_tariff_2': forms.fields.IntegerField,
                    'rural_tariff_3': forms.fields.IntegerField,
                }
                for value, excepted in form_fields.items():
                    with self.subTest(value=value):
                        form_field = response.context.get('form').fields.get(value)
                        self.assertIsInstance(form_field, excepted)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
        cls.points_list=[]
        for point in range(NUMBER_OF_TEST_POINTS):
            cls.points_list.append(ElectricityMeteringPoint.objects.create(
                constant_losses = 0,
                contract = cls.contract,
                name = f'electricity_metering_point{point}',
                location = 'location',
                losses = 0,
                margin = 0,
                power_supply = 'power_supply',
                tariff = 'tariff-free',
                transformation_coefficient = 1,
                type_of_accounting = 'Calculation accounting',
            ))

    def setUp(self):
        self.guest_client = Client()

    def test_first_page_points_records(self):
        """Checking the number of points on the first and last pages"""
        response_first_page = self.guest_client.get(reverse('accounting:points_list'))
        self.assertEqual(len(response_first_page.context['page_obj']), NUMBER_OF_OUTPUT_POINTS)
        response_last_page = self.guest_client.get(reverse('accounting:points_list') + '?page=-1')
        self.assertEqual(len(response_last_page.context['page_obj']), NUMBER_OF_TEST_POINTS % NUMBER_OF_OUTPUT_POINTS)
