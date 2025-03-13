import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from counterparties.models import (Comment,
                                   Contract,
                                   Counterparty,
                                   Document as Counterparties_Document)
from electricity_accounting.models import ElectricityMeteringPoint


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ElectricityAccountingModelTest(TestCase):
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
        cls.document = Counterparties_Document.objects.create(
            contract = cls.contract,
            conclusion_date = '2001-01-01',
            title = 'Title',
            file = SimpleUploadedFile('test_file.txt', b'content')
        )
        cls.comment = Comment.objects.create(
            author = cls.user,
            text = 'Long comment for testing',
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

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
    
    def test_models_have_correct_object_names(self):
        point_str = ElectricityAccountingModelTest.point.__str__()
        point_text = ElectricityAccountingModelTest.point.name
        self.assertEqual(point_str, point_text, 'point_error')
