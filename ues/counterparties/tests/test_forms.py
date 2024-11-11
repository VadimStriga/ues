from http import HTTPStatus
import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from counterparties.models import (Document,
                                   Comment,
                                   Contract,
                                   Counterparty)


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
TEST_CACHE_SETTING = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

User = get_user_model()


@override_settings(CACHES=TEST_CACHE_SETTING, MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CounterpartyCreateForm(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            email='ivan@email.ru',
            first_name='Ivan',
            middle_name='Ivanovich',
            last_name='Ivanov',
            letter_of_attorney='Attorney',
            password='password',
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
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(CounterpartyCreateForm.user)
        self.author_client = Client()
        self.author_client.force_login(
            CounterpartyCreateForm.counterparty_comment.author)
        self.guest_client = Client()

    def test_create_and_edit_counterparty(self):
        """A valid form creates and edits a counterparty."""
        counterparty_count = Counterparty.objects.count()
        templates_pages_names = [
            # reverse('counterparties:counterparty_edit',
            #         kwargs={'counterparty_id': f'{self.counterparty.id}'}),
            reverse('counterparties:counterparty_create'),
        ]
        for reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                if reverse_name == reverse('counterparties:counterparty_create'):
                    full_name = 'Test_Company',
                    short_name = 'TC',
                    address = '000000, Test city',
                    phone_number = '+71234567890',
                    email = 'test@email.ru',
                    main_state_registration_number = '1234567890112',
                    tax_identification_number = '1234567891',
                    registration_reason_code = '123456790',
                    job_title = 'Test_Director',
                    person_full_name = 'Test Name',
                    reverse_redirect = reverse(
                        'counterparties:counterparty_detail',
                        kwargs={'counterparty_id': '2'}
                    )
                    counterparty_count += 1
                else:
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
                    reverse_redirect = reverse(
                        'counterparties:counterparty_detail',
                        kwargs={'counterparty_id': f'{self.counterparty.id}'}
                    )
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
                    reverse_name,
                    data=form_data,
                    follow=True
                )
                # I do not understand why during the test, the redirect_chain
                # is lost for reverse_name, which is in second place in
                # tempaltes_pages_names.
                self.assertRedirects(response, reverse_redirect)
                self.assertEqual(Counterparty.objects.count(),
                                 counterparty_count)
                if reverse_name == reverse('counterparties:counterparty_create'):
                    self.assertTrue(
                        Counterparty.objects.filter(full_name='Test_Company'
                                                    ).exists()
                    )
                else:
                    self.assertTrue(
                        Counterparty.objects.filter(full_name='Test_Edit_Company'
                                                    ).exists()
                    )

    def test_create_and_edit_contract(self):
        """A valid form creates and edits a contract."""
        contract_count = Contract.objects.count()
        templates_pages_names = [
            reverse('counterparties:contract_create',
                    kwargs={'counterparty_id': f'{self.counterparty.id}'}),
            reverse('counterparties:contract_edit',
                    kwargs={'contract_id': f'{self.contract.id}'}),
        ]
        for reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                if reverse_name == reverse(
                    'counterparties:contract_create',
                    kwargs={'counterparty_id': f'{self.counterparty.id}'}
                ):
                    title = 'Test_create_title'
                    conclusion_date = '2001-01-01'
                    contract_price = '1000000'
                    purchase_code = '1234567890'
                    description = 'Test create hard work'
                    сompletion_date = '2001-01-01'
                    actual_cost = '999000'
                    reverse_redirect = reverse(
                        'counterparties:contract_detail',
                        kwargs={'contract_id': '2'},
                    )
                    contract_count += 1
                else:
                    title = 'Test_edit_title'
                    conclusion_date = '2001-01-01'
                    contract_price = '1000000'
                    purchase_code = '1234567890'
                    description = 'Test edit hard work'
                    сompletion_date = '2001-01-01'
                    actual_cost = '999000'
                    reverse_redirect = reverse(
                        'counterparties:contract_detail',
                        kwargs={'contract_id': f'{self.contract.id}'},
                    )
                form_data = {
                    'title': title,
                    'conclusion_date': conclusion_date,
                    'contract_price': contract_price,
                    'purchase_code': purchase_code,
                    'description': description,
                    'сompletion_date': сompletion_date,
                    'actual_cost': actual_cost,
                }
                response = self.authorized_client.post(
                    reverse_name,
                    data=form_data,
                    follow=True,
                )
                self.assertRedirects(response, reverse_redirect)
                self.assertEqual(Contract.objects.count(), contract_count)
                if reverse_name == reverse(
                    'counterparties:contract_create',
                    kwargs={'counterparty_id': f'{self.counterparty.id}'}
                ):
                    self.assertTrue(
                        Contract.objects.filter(
                            title='Test_create_title'
                        ).exists()
                    )
                else:
                    self.assertTrue(
                        Contract.objects.filter(
                            description='Test edit hard work'
                        ).exists()
                    )

    def test_create_and_edit_for_nonauthorized_user(self):
        """The creation and editing pages are not accessible to
        unauthorized users to the user.
        """
        templates_pages_names = [
            reverse('counterparties:counterparty_edit',
                    kwargs={'counterparty_id': f'{self.counterparty.id}'}),
            reverse('counterparties:counterparty_create'),
            reverse('counterparties:contract_create',
                    kwargs={'counterparty_id': f'{self.counterparty.id}'}),
            reverse('counterparties:contract_edit',
                    kwargs={'contract_id': f'{self.contract.id}'}),
        ]
        for reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_create_and_edit_counterpary_nonauthorized_user(self):
        """An unauthorized user cannot create or edit counterparties."""
        counterparty_count = Counterparty.objects.count()
        templates_pages_names = [
            reverse('counterparties:counterparty_edit',
                    kwargs={'counterparty_id': f'{self.counterparty.id}'}),
            reverse('counterparties:counterparty_create'),
        ]
        for reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                form_data = {
                    'full_name': 'Nonauthorized User',
                    'short_name': 'NU',
                    'address': 'www.leningrad-stp.ru',
                    'phone_number': '+71234567890',
                    'email': 'anonymous@usr.com',
                    'main_state_registration_number': '1234567890111',
                    'tax_identification_number': '1234567890',
                    'registration_reason_code': '123456789',
                    'job_title': 'anonymous',
                    'person_full_name': 'nonauthorized user',
                }
                response = self.guest_client.post(
                    reverse_name,
                    data=form_data,
                    follow=True
                )
                self.assertEqual(Counterparty.objects.count(),
                                 counterparty_count)
                self.assertFalse(
                    Counterparty.objects.filter(
                        person_full_name='nonauthorized user'
                    ).exists()
                )
                if reverse_name == reverse('counterparties:counterparty_create'):
                    self.assertRedirects(
                        response,
                        '/auth/login/?next=/counterparties/create/'
                    )
                else:
                    self.assertRedirects(
                        response,
                        f'/auth/login/?next=/counterparties/{self.counterparty.id}/edit/'
                    )

    def test_create_and_edit_contract_nonauthorized_user(self):
        """An unauthorized user cannot create or edit contacts."""
        contracts_count = Contract.objects.count()
        templates_pages_names = [
            reverse('counterparties:contract_create',
                    kwargs={'counterparty_id': f'{self.counterparty.id}'}),
            reverse('counterparties:contract_edit',
                    kwargs={'contract_id': f'{self.contract.id}'}),
        ]
        for reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                form_data = {
                    'title': 'nonauthorized_user_title',
                    'conclusion_date': '2001-01-01',
                    'contract_price': '0',
                    'purchase_code': '1234567890',
                    'description': 'nonauthorized user good work',
                    'сompletion_date': '2001-01-01',
                    'actual_cost': '0',
                }
                response = self.guest_client.post(
                    reverse_name,
                    data=form_data,
                    follow=True
                )
                self.assertEqual(Contract.objects.count(), contracts_count)
                self.assertFalse(
                    Contract.objects.filter(
                        title='nonauthorized_user_title'
                    ).exists()
                )
                if reverse_name == reverse(
                    'counterparties:contract_create',
                    kwargs={'counterparty_id': f'{self.counterparty.id}'}
                ):
                    self.assertRedirects(
                        response,
                        f'/auth/login/?next=/counterparties/{self.counterparty.id}/contract_create/'
                    )
                else:
                    self.assertRedirects(
                        response,
                        f'/auth/login/?next=/counterparties/contract_detail/{self.contract.id}/edit/'
                    )

    def test_create_comment(self):
        """A valid form creates a comment."""
        comments_count = Comment.objects.count()
        templates_reverse_names = [
            reverse(
                'counterparties:comment_counterparty_create',
                kwargs={'counterparty_id': f'{self.counterparty.id}'}
            ),
            reverse(
                'counterparties:comment_contract_create',
                kwargs={'contract_id': f'{self.contract.id}'}
            ),
        ]
        form_data = {
            'text': 'test_comment'
        }
        for reverse_name in templates_reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.post(
                    reverse_name,
                    data=form_data,
                    follow=True,
                )
                if reverse_name == reverse(
                    'counterparties:comment_counterparty_create',
                    kwargs={'counterparty_id': f'{self.counterparty.id}'}
                ):
                    self.assertRedirects(
                        response,
                        reverse(
                            'counterparties:counterparty_detail',
                            kwargs={
                                'counterparty_id': f'{self.counterparty.id}'},
                        )
                    )
                else:
                    self.assertRedirects(
                        response,
                        reverse('counterparties:contract_detail',
                                kwargs={'contract_id': f'{self.contract.id}'},)
                    )
                comments_count += 1
                self.assertEqual(Comment.objects.count(), comments_count)
                self.assertContains(response, 'test_comment')

    def test_do_not_create_comment(self):
        """A valid form does not create a comment."""
        comments_count = Comment.objects.count()
        templates_reverse_names = [
            reverse(
                'counterparties:comment_counterparty_create',
                kwargs={'counterparty_id': f'{self.counterparty.id}'}
            ),
            reverse(
                'counterparties:comment_contract_create',
                kwargs={'contract_id': f'{self.contract.id}'}
            ),
        ]
        form_data = {
            'text': 'test_comment'
        }
        for reverse_name in templates_reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.post(
                    reverse_name,
                    data=form_data,
                    follow=True,
                )
                self.assertEqual(Comment.objects.count(), comments_count)
                self.assertNotContains(response, 'test_comment')
