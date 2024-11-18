import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from counterparties.models import Comment, Contract, Counterparty, Document


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CounterpartiesModelTest(TestCase):
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
        cls.document = Document.objects.create(
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

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_models_have_correct_object_names(self):
        """Check that __str__ is working correctly for the models."""
        comment_str = CounterpartiesModelTest.comment.__str__()
        comment_text = CounterpartiesModelTest.comment.text[:20]
        contract_str = CounterpartiesModelTest.contract.__str__()
        contract_title = CounterpartiesModelTest.contract.title
        counterparty_str = CounterpartiesModelTest.counterparty.__str__()
        counterparty_short_name = CounterpartiesModelTest.counterparty.short_name
        document_str = CounterpartiesModelTest.document.__str__()
        document_title = CounterpartiesModelTest.document.title
        self.assertEqual(comment_str, comment_text, 'comment error')
        self.assertEqual(contract_str, contract_title, 'contract error')
        self.assertEqual(counterparty_str, counterparty_short_name, 'counterparty error')
        self.assertEqual(document_str, document_title, 'document error')
