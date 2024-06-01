from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import ContactRequest


class ContactViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')
        self.home_url = reverse('home')  # Add home URL for redirection check

    def test_get_contact_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    @patch('contact.views.send_mail')
    def test_post_contact_view(self, mock_send_mail):
        data = {
            'full_name': 'John Doe',
            'email': 'john.doe@example.com',
            'subject': 'Test Subject',
            'message': 'Test message.',
        }
        file_data = {
            'file_upload': SimpleUploadedFile("file.txt", b"file_content")
        }
        
        response = self.client.post(self.url, data, **file_data)
        
        self.assertEqual(response.status_code, 302)  # Check redirection
        self.assertRedirects(response, self.home_url)  # Update to check redirection to home
        self.assertTrue(ContactRequest.objects.exists())
        
        contact_request = ContactRequest.objects.first()
        self.assertEqual(contact_request.full_name, data['full_name'])
        self.assertEqual(contact_request.email, data['email'])
        self.assertEqual(contact_request.subject, data['subject'])
        self.assertEqual(contact_request.message, data['message'])

        # Check that email was sent
        mock_send_mail.assert_called_once()
        email_subject = mock_send_mail.call_args[0][0]
        email_body = mock_send_mail.call_args[0][1]
        email_from = mock_send_mail.call_args[0][2]
        email_to = mock_send_mail.call_args[0][3]

        self.assertIn(contact_request.full_name, email_body)
        self.assertEqual(email_from, settings.DEFAULT_FROM_EMAIL)
        self.assertIn(data['email'], email_to)

        # Check for success message in the POST response
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'Your contact request has been submitted. A confirmation email has been sent to {data["email"]}.')
