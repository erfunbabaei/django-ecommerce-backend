from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Product
from orders.models import Order, OrderItem

User = get_user_model()


class AdminPanelTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123"
        )

        self.user = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            password="customer123"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=100,
            stock=10,
            seller=self.admin_user
        )

        self.order = Order.objects.create(
            user=self.user,
            status="completed"
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=100
        )


    # -------------------
    # Sales report test
    # -------------------
    def test_sales_report_view(self):
        url = reverse("sales_report")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("total_sales", response.json())
        self.assertIn("total_revenue", response.json())
        self.assertEqual(response.json()["total_sales"], 1)
        self.assertEqual(response.json()["total_revenue"], 200)

    # -------------------
    # Product Management Test
    # -------------------
    def test_admin_can_list_products(self):
        url = reverse("admin-product-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_admin_can_create_product(self):
        url = reverse("admin-product-list-create")
        data = {
            "name": "New Product",
            "description": "Desc",
            "price": 50,
            "stock": 5,
            "category": "other"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # -------------------
    # User management test
    # -------------------
    def test_admin_can_list_users(self):
        url = reverse("admin-user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # -------------------
    # Order Management Test
    # -------------------
    def test_admin_can_list_orders(self):
        url = reverse("admin-order-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
