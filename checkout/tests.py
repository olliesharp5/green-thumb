from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from unittest.mock import patch
from .models import Order, OrderLineItem
from profiles.models import UserProfile
from products.models import Product, Category
import json

class CheckoutViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', price=10.00, category=self.category)
        self.order_data = {
            'full_name': 'Test User',
            'email': 'testuser@example.com',
            'phone_number': '1234567890',
            'country': 'US',
            'postcode': '12345',
            'town_or_city': 'Test City',
            'street_address1': '123 Test Street',
            'street_address2': '',
            'county': 'Test County',
        }
        self.user_profile = UserProfile.objects.create(user=self.user)

    @patch('checkout.views.stripe.PaymentIntent.modify')
    def test_cache_checkout_data_success(self, mock_modify):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('cache_checkout_data'), {
            'client_secret': 'pi_12345_secret_12345',
            'save_info': 'on',
        })
        self.assertEqual(response.status_code, 200)
        mock_modify.assert_called_once()

    @patch('checkout.views.stripe.PaymentIntent.modify')
    def test_cache_checkout_data_exception(self, mock_modify):
        mock_modify.side_effect = Exception("Test Exception")
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('cache_checkout_data'), {
            'client_secret': 'pi_12345_secret_12345',
            'save_info': 'on',
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Test Exception', response.content.decode())

    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_checkout_get(self, mock_create):
        mock_create.return_value.client_secret = 'test_secret'
        self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['cart'] = {str(self.product.id): 1}
        session.save()
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIn('order_form', response.context)
        self.assertIn('stripe_public_key', response.context)
        self.assertIn('client_secret', response.context)

    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_checkout_post_valid(self, mock_create):
        mock_create.return_value.client_secret = 'test_secret'
        self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['cart'] = {str(self.product.id): 1}
        session.save()
        response = self.client.post(reverse('checkout'), {
            **self.order_data,
            'client_secret': 'pi_12345_secret_12345',
        })
        self.assertRedirects(response, reverse('checkout_success', args=[Order.objects.first().order_number]))

    def test_checkout_post_invalid(self):
        self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['cart'] = {str(self.product.id): 1}
        session.save()
        invalid_order_data = self.order_data.copy()
        invalid_order_data['full_name'] = ''  # Invalid data
        response = self.client.post(reverse('checkout'), invalid_order_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        messages = list(response.context['messages'])
        self.assertTrue(any('There was an error with your form.' in message.message for message in messages))

    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_checkout_empty_cart(self, mock_create):
        mock_create.return_value.client_secret = 'test_secret'
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('checkout'))
        self.assertRedirects(response, reverse('products'))
        from django.contrib.messages import get_messages
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("There's nothing in your cart at the moment" in message.message for message in messages))

    def test_checkout_success(self):
        self.client.login(username='testuser', password='testpass')
        order = Order.objects.create(
            user_profile=self.user_profile,
            full_name='Test User',
            email='testuser@example.com',
            phone_number='1234567890',
            country='US',
            postcode='12345',
            town_or_city='Test City',
            street_address1='123 Test Street',
            street_address2='',
            county='Test County',
            stripe_pid='pi_12345'
        )
        response = self.client.get(reverse('checkout_success', args=[order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertIn('order', response.context)
        messages = list(response.context['messages'])
        self.assertTrue(any(f'Order successfully processed!             Your order number is {order.order_number}. A confirmation             email will be sent to {order.email}.' in message.message for message in messages))

if __name__ == '__main__':
    TestCase.main()
