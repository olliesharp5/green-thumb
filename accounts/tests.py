import io
from PIL import Image
import logging

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from profiles.models import UserProfile, Wishlist
from .forms import RegistrationForm, GardenerForm


logger = logging.getLogger(__name__)

class RegisterViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def generate_test_image_file(self):
        # Create a simple image file
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100), color=(73, 109, 137))
        image.save(file, 'jpeg')
        file.name = 'test_image.jpg'
        file.seek(0)
        return SimpleUploadedFile(file.name, file.read(), content_type='image/jpeg')

    def test_get_register_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertIsInstance(response.context['user_form'], RegistrationForm)
        self.assertIsInstance(response.context['gardener_form'], GardenerForm)

    def test_post_register_regular_user_success(self):
        data = {
            'username': 'regularuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'regularuser@example.com',
            'gardener': False
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('home'))
        user = User.objects.get(username='regularuser')
        self.assertTrue(UserProfile.objects.filter(user=user, role='RU').exists())
        self.assertTrue(Wishlist.objects.filter(user__user=user).exists())

    def test_post_register_gardener_success(self):
        image = self.generate_test_image_file()
        data = {
            'username': 'gardeneruser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'gardeneruser@example.com',
            'gardener': True,
            'profile_image': image,
            'display_name': 'Gardener Display Name',
            'location': 'Gardener Location',
            'about': 'About the gardener'
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('home'))
        user = User.objects.get(username='gardeneruser')
        self.assertTrue(UserProfile.objects.filter(user=user, role='GR').exists())
        self.assertTrue(Wishlist.objects.filter(user__user=user).exists())

    def test_post_register_user_form_invalid(self):
        data = {
            'username': 'invaliduser',
            'password1': 'testpassword',
            'password2': 'differentpassword',
            'email': 'invaliduser@example.com',
            'gardener': False
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertIsInstance(response.context['user_form'], RegistrationForm)
        self.assertIsInstance(response.context['gardener_form'], GardenerForm)
        self.assertTrue(response.context['user_form'].errors)

    def test_post_register_gardener_form_invalid(self):
        image = self.generate_test_image_file()
        data = {
            'username': 'invalidgardener',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'invalidgardener@example.com',
            'gardener': True,
            'profile_image': image,
            'display_name': '',  # Missing display name
            'location': '',  # Missing location
            'about': ''  # Missing about
        }
        response = self.client.post(self.url, data)
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response context: {response.context}")
        logger.debug(f"User form errors: {response.context['user_form'].errors}")
        logger.debug(f"Gardener form errors: {response.context['gardener_form'].errors}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertIsInstance(response.context['user_form'], RegistrationForm)
        self.assertIsInstance(response.context['gardener_form'], GardenerForm)
        self.assertTrue(response.context['gardener_form'].errors)
