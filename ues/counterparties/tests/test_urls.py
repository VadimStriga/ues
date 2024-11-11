from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from counterparties.models import Comment, Contract, Counterparty, Document


User = get_user_model()


class CounterpartiesURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = User.objects.create(
            email = 'ivan@email.ru',
            first_name = 'Ivan',
            middle_name = 'Ivanovich',
            last_name = 'Ivanov',
            letter_of_attorney = 'Attorney',
            post = 'employee',
        )
        cls.user2 = User.objects.create(
            email = 'peter@email.ru',
            first_name = 'Peter',
            middle_name = 'Petrovich',
            last_name = 'Petrov',
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
            title = '123P-15Hj',
            conclusion_date = '2001-01-01',
            contract_price = '12345',
            purchase_code = '1234567890',
            description = 'Hard work',
            сompletion_date = '2001-01-01',
            actual_cost = '12345',
        )
        cls.document = Document.objects.create(
            contract = cls.contract,
            conclusion_date = '2001-01-01',
            title = 'Document title',
            file = SimpleUploadedFile('test_file.txt', b'content')
        )
        cls.contract_comment = Comment.objects.create(
            author = cls.user1,
            text = 'Long contract comment for testing',
            created = '2001-01-01',
            updated = '2001-01-01',
            content_type = ContentType.objects.get_for_model(Contract),
            object_id = cls.contract.id,
        )
        cls.counterparty_comment = Comment.objects.create(
            author = cls.user1,
            text = 'Long counterparty comment for testing',
            created = '2001-01-01',
            updated = '2001-01-01',
            content_type = ContentType.objects.get_for_model(Counterparty),
            object_id = cls.counterparty.id,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(CounterpartiesURLTests.user2)
        self.author_client = Client()
        self.author_client.force_login(CounterpartiesURLTests.contract_comment.author)

    def test_urls(self):
        """Access to the page and the template depends on the user."""
        cache.clear()
        templates_url_names = {
            f'/counterparties/contract_detail/{self.contract.id}/document_create/': 'counterparties/contract_detail.html',
            f'/counterparties/contract_detail/{self.contract.id}/document/{self.document.id}/delete/': 'counterparties/contract_detail.html',
            f'/counterparties/{self.counterparty.id}/contract_create/': 'counterparties/contract_create.html',
            f'/counterparties/contract_detail/{self.contract.id}/':'counterparties/contract_detail.html',
            f'/counterparties/contract_detail/{self.contract.id}/edit/': 'counterparties/contract_create.html',
            '/counterparties/contracts_list/': 'counterparties/contracts_list.html',
            '/counterparties/create/': 'counterparties/counterparty_create.html',
            f'/counterparties/{self.counterparty.id}/': 'counterparties/counterperty_detail.html',
            f'/counterparties/{self.counterparty.id}/edit/': 'counterparties/counterparty_create.html',
            '/counterparties/counterparties_list/': 'counterparties/counterparties_list.html',
            f'/counterparties/contract_detail/{self.contract.id}/comments/create/': 'counterparties/contract_detail.html',
            f'/counterparties/contract_detail/{self.contract.id}/comments/{self.contract_comment.id}/edit/': 'counterparties/comment_edit.html',
            f'/counterparties/contract_detail/{self.contract.id}/comments/{self.contract_comment.id}/delete/':'counterparties/contract_detail.html',
            f'/counterparties/{self.counterparty.id}/comments/create/': 'counterparties/counterperty_detail.html',
            f'/counterparties/{self.counterparty.id}/comments/{self.counterparty_comment.id}/edit/': 'counterparties/comment_edit.html',
            f'/counterparties/{self.counterparty.id}/comments/{self.counterparty_comment.id}/delete/': 'counterparties/counterperty_detail.html',
            f'/counterparties/{self.counterparty.id}/contract_detail/{self.contract.id}/delete/': 'counterparties/contract_detail.html',
            f'/counterparties/{self.counterparty.id}/delete/': 'counterparties/counterperty_detail.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.author_client.get(address)
                if address == f'/counterparties/contract_detail/{self.contract.id}/document_create/':
                    self.assertRedirects(response, f'/counterparties/contract_detail/{self.contract.id}/')
                elif address == f'/counterparties/contract_detail/{self.contract.id}/document/{self.document.id}/delete/':
                    self.assertRedirects(response, f'/counterparties/contract_detail/{self.contract.id}/')
                elif address == f'/counterparties/{self.counterparty.id}/contract_detail/{self.contract.id}/delete/':
                    self.assertRedirects(response, f'/counterparties/{self.counterparty.id}/')
                elif address == f'/counterparties/contract_detail/{self.contract.id}/comments/create/':
                    self.assertRedirects(response, f'/counterparties/contract_detail/{self.contract.id}/')
                elif address == f'/counterparties/contract_detail/{self.contract.id}/comments/{self.contract_comment.id}/delete/':
                    self.assertRedirects(response, f'/counterparties/contract_detail/{self.contract.id}/')
                elif address == f'/counterparties/{self.counterparty.id}/comments/create/':
                    self.assertRedirects(response, f'/counterparties/{self.counterparty.id}/')
                elif address == f'/counterparties/{self.counterparty.id}/comments/{self.counterparty_comment.id}/delete/':
                    self.assertRedirects(response, f'/counterparties/{self.counterparty.id}/')
                elif address == f'/counterparties/{self.counterparty.id}/delete/':
                    self.assertRedirects(response, '/counterparties/counterparties_list/')
                else:
                    self.assertEqual(response.status_code, HTTPStatus.OK)
                    self.assertTemplateUsed(response, template)

                response = self.guest_client.get(address)
                if address == f'/counterparties/contract_detail/{self.contract.id}/document_create/':
                    self.assertRedirects(response, (f'/auth/login/?next={address}'))
                elif address == f'/counterparties/contract_detail/{self.contract.id}/document/{self.document.id}/delete/':
                    self.assertRedirects(response, (f'/auth/login/?next={address}'))
                elif address == f'/counterparties/contract_detail/{self.contract.id}/comments/create/':
                    self.assertRedirects(response, f'/auth/login/?next={address}')
                elif address == f'/counterparties/contract_detail/{self.contract.id}/comments/{self.contract_comment.id}/edit/':
                    self.assertRedirects(response, f'/auth/login/?next={address}')
                elif address == f'/counterparties/contract_detail/{self.contract.id}/comments/{self.contract_comment.id}/delete/':
                    self.assertRedirects(response, f'/auth/login/?next={address}')
                elif address == f'/counterparties/{self.counterparty.id}/contract_create/':
                    self.assertRedirects(response, (f'/auth/login/?next={address}'))
                elif address ==  f'/counterparties/contract_detail/{self.contract.id}/edit/':
                    self.assertRedirects(response, (f'/auth/login/?next={address}'))
                elif address == f'/counterparties/{self.counterparty.id}/contract_detail/{self.contract.id}/delete/':
                    self.assertRedirects(response, (f'/auth/login/?next={address}'))
                elif address == f'/counterparties/{self.counterparty.id}/comments/create/':
                    self.assertRedirects(response, f'/auth/login/?next={address}')
                elif address == f'/counterparties/{self.counterparty.id}/comments/{self.counterparty_comment.id}/edit/':
                    self.assertRedirects(response, f'/auth/login/?next={address}')
                elif address == f'/counterparties/{self.counterparty.id}/comments/{self.counterparty_comment.id}/delete/':
                    self.assertRedirects(response, f'/auth/login/?next={address}')
                elif address == '/counterparties/create/':
                    self.assertRedirects(response, f'/auth/login/?next={address}')
                elif address == f'/counterparties/{self.counterparty.id}/edit/':
                    self.assertRedirects(response, f'/auth/login/?next={address}')
                elif address == f'/counterparties/{self.counterparty.id}/delete/':
                    self.assertRedirects(response, f'/auth/login/?next={address}')
                else:
                    self.assertEqual(response.status_code, HTTPStatus.OK)
                    self.assertTemplateUsed(response, template)

                response = self.authorized_client.get(address)
                if address == f'/counterparties/contract_detail/{self.contract.id}/document_create/':
                    self.assertRedirects(response, f'/counterparties/contract_detail/{self.contract.id}/')
                elif address == f'/counterparties/contract_detail/{self.contract.id}/document/{self.document.id}/delete/':
                    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)  # Actually, I was expecting a redirect here.
                elif address == f'/counterparties/contract_detail/{self.contract.id}/comments/create/':
                    self.assertRedirects(response, f'/counterparties/contract_detail/{self.contract.id}/')
                elif address == f'/counterparties/contract_detail/{self.contract.id}/comments/{self.contract_comment.id}/edit/':
                    self.assertRedirects(response, f'/counterparties/contract_detail/{self.contract.id}/')
                elif address == f'/counterparties/{self.counterparty.id}/comments/create/':
                    self.assertRedirects(response, f'/counterparties/{self.counterparty.id}/')
                elif address == f'/counterparties/{self.counterparty.id}/comments/{self.counterparty_comment.id}/edit/':
                    self.assertRedirects(response, f'/counterparties/{self.counterparty.id}/')
                elif address == f'/counterparties/{self.counterparty.id}/comments/{self.counterparty_comment.id}/delete/':
                    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)  # Actually, I was expecting a redirect here.
                elif address == f'/counterparties/contract_detail/{self.contract.id}/comments/{self.contract_comment.id}/delete/':
                    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)  # Actually, I was expecting a redirect here.
                elif address == f'/counterparties/{self.counterparty.id}/contract_detail/{self.contract.id}/delete/':
                    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)  # Actually, I was expecting a redirect here.
                elif address == f'/counterparties/{self.counterparty.id}/delete/':
                    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)  # Actually, I was expecting a redirect here.
                else:
                    self.assertEqual(response.status_code, HTTPStatus.OK)
                    self.assertTemplateUsed(response, template)

    def test_404(self):
        """Page 404 gives you a custom template."""
        respone = self.guest_client.get('/any/unknow/page/')
        self.assertTemplateUsed(respone, 'core/404.html')
