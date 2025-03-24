from datetime import date
import shutil
import tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from counterparties.models import Comment, Contract, Counterparty, Document
from counterparties.views import (NUMBER_OF_OUTPUT_CONTRACTS,
                                  NUMBER_OF_OUTPUT_COUNTERPARTIES)


User = get_user_model()


NUMBER_OF_TESTS_CONTRACTS = NUMBER_OF_OUTPUT_CONTRACTS + 5
NUMBER_OF_TESTS_COUNTERPARTIES = NUMBER_OF_OUTPUT_COUNTERPARTIES + 5
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CounterpartiesPagesTests(TestCase):
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
        cls.counterparty = Counterparty.objects.create(
            full_name='Limited Liability Company "Company"',
            short_name='LLC "Company"',
            address='000000, Ivanovsk city',
            phone_number='+71234567890',
            email='llc@email.ru',
            main_state_registration_number='1234567890111',
            tax_identification_number='1234567890',
            registration_reason_code='123456789',
            job_title='director',
            person_full_name='Ivanov Ivan Ivanovich',
        )
        cls.contract = Contract.objects.create(
            counterparty=cls.counterparty,
            title='123P-15Hj',
            conclusion_date='2001-01-01',
            contract_price='12345',
            purchase_code='1234567890',
            description='Hard work',
            сompletion_date='2001-01-01',
            actual_cost='12345',
        )
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
            content_type='image/gif'
        )
        cls.document = Document.objects.create(
            contract=cls.contract,
            conclusion_date='2001-01-01',
            title='Document title',
            file=uploaded
        )
        cls.contract_comment = Comment.objects.create(
            author=cls.user,
            text='Long comment for testing',
            created='2001-01-01',
            updated='2001-01-01',
            content_type=ContentType.objects.get_for_model(Contract),
            object_id=cls.contract.id,
        )
        cls.counterparty_comment = Comment.objects.create(
            author=cls.user,
            text='Long comment for testing',
            created='2001-01-01',
            updated='2001-01-01',
            content_type=ContentType.objects.get_for_model(Counterparty),
            object_id=cls.counterparty.id,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(CounterpartiesPagesTests.user)
        self.author_client = Client()
        self.author_client.force_login(
            CounterpartiesPagesTests.counterparty_comment.author)

    def test_pages_uses_correct_template(self):
        """The URL uses the appropriate template."""
        template_pages_names = {
            reverse('counterparties:contract_create',
                    kwargs={'counterparty_id': f'{self.counterparty.id}'}
                    ): 'counterparties/contract_create.html',
            reverse('counterparties:contract_detail',
                    kwargs={'contract_id': f'{self.contract.id}'}
                    ): 'counterparties/contract_detail.html',
            reverse('counterparties:contract_edit',
                    kwargs={'contract_id': f'{self.contract.id}'}
                    ): 'counterparties/contract_create.html',
            reverse('counterparties:contracts_list'
                    ): 'counterparties/contracts_list.html',
            reverse('counterparties:counterparty_create'
                    ): 'counterparties/counterparty_create.html',
            reverse('counterparties:counterparty_detail',
                    kwargs={'counterparty_id': f'{self.counterparty.id}'}
                    ): 'counterparties/counterperty_detail.html',
            reverse('counterparties:counterparty_edit',
                    kwargs={'counterparty_id': f'{self.counterparty.id}'}
                    ): 'counterparties/counterparty_create.html',
            reverse('counterparties:counterparties_list'
                    ): 'counterparties/counterparties_list.html',
            reverse('counterparties:comment_contract_edit',
                    kwargs={'contract_id': f'{self.contract.id}',
                            'comment_id': f'{self.contract_comment.id}'}
                    ): 'counterparties/comment_edit.html',
            reverse('counterparties:comment_counterparty_edit',
                    kwargs={'counterparty_id': f'{self.counterparty.id}',
                            'comment_id': f'{self.contract_comment.id}'}
                    ): 'counterparties/comment_edit.html',
        }
        for revers_name, template in template_pages_names.items():
            with self.subTest(revers_name=revers_name):
                response = self.authorized_client.get(revers_name)
                self.assertTemplateUsed(response, template)

    def test_contract_create_contract_edit_show_correct_context(self):
        """contract_create and contract_edit templates formed with the
        right context.
        """
        template_pages_names = [
            reverse('counterparties:contract_create',
                    kwargs={'counterparty_id': f'{self.counterparty.id}'}),
            reverse('counterparties:contract_edit',
                    kwargs={'contract_id': f'{self.contract.id}'}),
        ]
        for reverse_name in template_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                form_field = {
                    'title': forms.fields.CharField,
                    'conclusion_date': forms.fields.DateField,
                    'contract_price': forms.fields.IntegerField,
                    'purchase_code': forms.fields.CharField,
                    'description': forms.fields.CharField,
                    'сompletion_date': forms.fields.DateField,
                    'actual_cost': forms.fields.IntegerField,
                }
            for value, excepted in form_field.items():
                with self.subTest(value=value):
                    form_field = response.context.get('form').fields.get(value)
                    self.assertIsInstance(form_field, excepted)

    def test_contract_detail_show_correct_context(self):
        """contract_detail template formed with the right context."""
        response = self.authorized_client.get(reverse(
            'counterparties:contract_detail',
            kwargs={'contract_id': f'{self.contract.id}'})
        )
        self.assertEqual(response.context.get('contract').title, '123P-15Hj')
        self.assertEqual(response.context.get(
            'contract').conclusion_date, date(2001, 1, 1))
        self.assertEqual(response.context.get(
            'contract').contract_price, 12345)
        self.assertEqual(response.context.get(
            'contract').purchase_code, '1234567890')
        self.assertEqual(response.context.get(
            'contract').description, 'Hard work')
        self.assertEqual(response.context.get(
            'contract').сompletion_date, date(2001, 1, 1))
        self.assertEqual(response.context.get('contract').actual_cost, 12345)

    def test_contracts_list_show_correct_context(self):
        """contract_list template formed with the right context."""
        template_pages_names = [
            reverse('counterparties:contracts_list'),
        ]
        for reverse_name in template_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                first_contract = response.context['page_obj'][0]
                title = first_contract.title
                conclusion_date = first_contract.conclusion_date
                contract_price = first_contract.contract_price
                purchase_code = first_contract.purchase_code
                description = first_contract.description
                сompletion_date = first_contract.сompletion_date
                actual_cost = first_contract.actual_cost
                self.assertEqual(title, '123P-15Hj')
                self.assertEqual(conclusion_date, date(2001, 1, 1))
                self.assertEqual(contract_price, 12345)
                self.assertEqual(purchase_code, '1234567890')
                self.assertEqual(description, 'Hard work')
                self.assertEqual(сompletion_date, date(2001, 1, 1))
                self.assertEqual(actual_cost, 12345)

    def test_counterparty_create_counterparty_edit_show_correct_context(self):
        """counterparty_create and counterparty_edit templates formed with
        the right context.
        """
        template_pages_names = [
            reverse('counterparties:counterparty_create'),
            reverse('counterparties:counterparty_edit',
                    kwargs={'counterparty_id': f'{self.counterparty.id}'}),
        ]
        for reverse_name in template_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                form_field = {
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
            for value, excepted in form_field.items():
                with self.subTest(value=value):
                    form_field = response.context.get('form').fields.get(value)
                    self.assertIsInstance(form_field, excepted)

    def test_counterparty_detail_show_correct_context(self):
        """counterparty_detail template formed with the right context."""
        response = self.authorized_client.get(reverse(
            'counterparties:counterparty_detail',
            kwargs={'counterparty_id': f'{self.counterparty.id}'})
        )
        self.assertEqual(response.context.get(
            'counterparty').full_name, 'Limited Liability Company "Company"')
        self.assertEqual(response.context.get(
            'counterparty').short_name, 'LLC "Company"')
        self.assertEqual(response.context.get(
            'counterparty').address, '000000, Ivanovsk city')
        self.assertEqual(response.context.get(
            'counterparty').phone_number, '+71234567890')
        self.assertEqual(response.context.get(
            'counterparty').email, 'llc@email.ru')
        self.assertEqual(response.context.get(
            'counterparty').main_state_registration_number, 1234567890111)
        self.assertEqual(response.context.get(
            'counterparty').tax_identification_number, 1234567890)
        self.assertEqual(response.context.get(
            'counterparty').registration_reason_code, 123456789)
        self.assertEqual(response.context.get(
            'counterparty').job_title, 'director')
        self.assertEqual(response.context.get(
            'counterparty').person_full_name, 'Ivanov Ivan Ivanovich')

    def test_counterparties_list_show_correct_context(self):
        """counterparty_list template formed with the right context."""
        template_pages_names = [
            reverse('counterparties:counterparties_list'),
        ]
        for reverse_name in template_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                first_counterparty = response.context['page_obj'][0]
                full_name = first_counterparty.full_name
                short_name = first_counterparty.short_name
                address = first_counterparty.address
                phone_number = first_counterparty.phone_number
                email = first_counterparty.email
                main_state_registration_number = first_counterparty.main_state_registration_number
                tax_identification_number = first_counterparty.tax_identification_number
                registration_reason_code = first_counterparty.registration_reason_code
                job_title = first_counterparty.job_title
                person_full_name = first_counterparty.person_full_name
                self.assertEqual(
                    full_name, 'Limited Liability Company "Company"')
                self.assertEqual(short_name, 'LLC "Company"')
                self.assertEqual(address, '000000, Ivanovsk city')
                self.assertEqual(phone_number, '+71234567890')
                self.assertEqual(email, 'llc@email.ru')
                self.assertEqual(main_state_registration_number, 1234567890111)
                self.assertEqual(tax_identification_number, 1234567890)
                self.assertEqual(registration_reason_code, 123456789)
                self.assertEqual(job_title, 'director')
                self.assertEqual(person_full_name, 'Ivanov Ivan Ivanovich')

    def test_comment_edit_show_correct_context(self):
        """comment_edit template formed with the right context."""
        template_pages_names = [
            reverse('counterparties:comment_contract_edit',
                    kwargs={'contract_id': f'{self.contract.id}',
                            'comment_id': f'{self.contract_comment.id}'}),
            reverse('counterparties:comment_counterparty_edit',
                    kwargs={'counterparty_id': f'{self.counterparty.id}',
                            'comment_id': f'{self.contract_comment.id}'}),
        ]
        for reverse_name in template_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.author_client.get(reverse_name)
                form_field = {
                    'text': forms.fields.CharField,
                }
            for value, excepted in form_field.items():
                with self.subTest(value=value):
                    form_field = response.context.get('form').fields.get(value)
                    self.assertIsInstance(form_field, excepted)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.counterparties_list=[]
        for counterparty in range(NUMBER_OF_TESTS_COUNTERPARTIES):
            cls.counterparties_list.append(Counterparty.objects.create(
                full_name=f'Test_counterpaty{counterparty}',
                short_name=f'TC{counterparty}',
                address='000000, ... City',
                phone_number='+71234567890',
                email='email@email.ru',
                main_state_registration_number=f'{1234567890111 + counterparty}',
                tax_identification_number=f'{1234567890 + counterparty}',
                registration_reason_code='123456789',
                job_title=f'director{counterparty}',
                person_full_name='Ivanov Ivan Ivanovich',
            ))
            cls.contracts_list = []
            for contract in range(NUMBER_OF_TESTS_CONTRACTS):
                cls.contracts_list.append(Contract.objects.create(
                    counterparty=cls.counterparties_list[0],
                    title=f'{contract}',
                    conclusion_date='2001-01-01',
                    contract_price='12345',
                    purchase_code='1234567890',
                    description='Hard work',
                    сompletion_date='2001-01-01',
                    actual_cost='12345',
                ))

    def setUp(self):
        self.guest_client = Client()

    def test_first_page_counterparties_records(self):
        """Checking the number of counterparties on the first and last pages"""
        response_first_page = self.guest_client.get(reverse('counterparties:counterparties_list'))
        self.assertEqual(len(response_first_page.context['page_obj']), NUMBER_OF_OUTPUT_COUNTERPARTIES)
        response_last_page = self.guest_client.get(reverse('counterparties:counterparties_list') + '?page=-1')
        self.assertEqual(len(response_last_page.context['page_obj']), NUMBER_OF_TESTS_COUNTERPARTIES % NUMBER_OF_OUTPUT_COUNTERPARTIES)

    def test_first_page_contracts_records(self):
        """Checking the number of contracts on the first and last pages"""
        response_first_page = self.guest_client.get(reverse('counterparties:contracts_list'))
        self.assertEqual(len(response_first_page.context['page_obj']), NUMBER_OF_OUTPUT_CONTRACTS)
        response_last_page = self.guest_client.get(reverse('counterparties:contracts_list') + '?page=-1')
        self.assertEqual(len(response_last_page.context['page_obj']), NUMBER_OF_TESTS_CONTRACTS % NUMBER_OF_OUTPUT_CONTRACTS)
