from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from .models import Product, ProductImage

class ProductModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='seller',
            password='testpass'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='A test product',
            price=100.00,
            stock=10,
            category='electronics',
            seller=self.user
        )
        self.image = ProductImage.objects.create(
            product=self.product,
            image=SimpleUploadedFile(
                name='test.jpg',
                content=b'',
                content_type='image/jpeg'
            ),
            uploaded_at=timezone.now()
        )

    def test_product_str(self):
        expected_str = f'{self.product.name} - {self.product.category}'
        self.assertEqual(str(self.product), expected_str)

    def test_product_fields(self):
        self.assertEqual(self.product.price, 100.00)
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(self.product.category, 'electronics')
        self.assertEqual(self.product.seller.username, 'seller')


class ProductImageModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='seller2',
            password='testpass'
        )
        self.product = Product.objects.create(
            name='Test Product 2',
            description='Another test product',
            price=200.00,
            stock=5,
            category='books',
            seller=self.user
        )
        self.image = ProductImage.objects.create(
            product=self.product,
            image=SimpleUploadedFile(
                name='test.jpg',
                content=b'',
                content_type='image/jpeg'
            ),
            uploaded_at=timezone.now()
        )

    def test_product_image_str(self):
        self.assertIn(self.product.name, str(self.image))
        self.assertIn('.jpg', str(self.image))
