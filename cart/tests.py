from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from products.models import Product, Category

class CartViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', price=10.00, category=self.category)

    def test_cart_view(self):
        response = self.client.get(reverse('cart_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')

    def test_add_to_cart(self):
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]), {
            'quantity': 2,
            'product_size': 'M',
            'from_product_page': 'true'
        }, follow=True)
        self.assertRedirects(response, reverse('product_detail', args=[self.product.id]))
        self.assertTrue('cart' in self.client.session)
        self.assertTrue(str(self.product.id) in self.client.session['cart'])
        self.assertTrue('M' in self.client.session['cart'][str(self.product.id)]['items_by_size'])
        self.assertEqual(self.client.session['cart'][str(self.product.id)]['items_by_size']['M'], 2)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Test Product size M has been added to your cart!')

    def test_update_cart(self):
        # First add to cart
        self.client.post(reverse('add_to_cart', args=[self.product.id]), {
            'quantity': 2,
            'product_size': 'M',
            'from_product_page': 'true'
        })
        # Then update the cart
        response = self.client.post(reverse('update_cart', args=[self.product.id]), {
            'quantity': 5,
            'size': 'M'
        }, follow=True)
        self.assertRedirects(response, reverse('cart_view'))
        self.assertEqual(self.client.session['cart'][str(self.product.id)]['items_by_size']['M'], 5)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[0]), 'Test Product size M has been added to your cart!')
        self.assertEqual(str(messages[1]), 'Quantity of Test Product size M in your cart has been updated!')

    def test_remove_from_cart(self):
        # First add to cart
        self.client.post(reverse('add_to_cart', args=[self.product.id]), {
            'quantity': 2,
            'product_size': 'M',
            'from_product_page': 'true'
        })
        # Then remove from cart
        response = self.client.post(reverse('remove_from_cart', args=[self.product.id]), {
            'size': 'M'
        }, follow=True)
        self.assertRedirects(response, reverse('cart_view'))
        self.assertFalse(str(self.product.id) in self.client.session['cart'])
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[0]), 'Test Product size M has been added to your cart!')
        self.assertEqual(str(messages[1]), 'Test Product size M has been removed from your cart!')
