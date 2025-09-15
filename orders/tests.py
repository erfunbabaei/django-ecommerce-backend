from django.test import TestCase
from django.contrib.auth import get_user_model
from products.models import Product
from .models import Cart, Order, OrderItem, Payment

User = get_user_model()

class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cartuser', password='testpass')
        self.product = Product.objects.create(
            name='Cart Product',
            description='For cart test',
            price=50.00,
            stock=20,
            category='books',
            seller=self.user
        )
        self.cart = Cart.objects.create(user=self.user, product=self.product, quantity=3)

    def test_cart_str(self):
        self.assertIn('cartuser', str(self.cart))
        self.assertIn('Cart Product', str(self.cart))
        self.assertIn('3', str(self.cart))

    def test_cart_fields(self):
        self.assertEqual(self.cart.quantity, 3)
        self.assertEqual(self.cart.product, self.product)
        self.assertEqual(self.cart.user, self.user)

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='orderuser', password='testpass')
        self.product = Product.objects.create(
            name='Order Product',
            description='For order test',
            price=80.00,
            stock=15,
            category='electronics',
            seller=self.user
        )
        self.order = Order.objects.create(user=self.user)
        self.order2 = Order.objects.create(user=self.user)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2, price=80.00)

    def test_order_str_and_status(self):
        self.assertIn('orderuser', str(self.order))
        self.assertEqual(self.order.status, 'pending')

    def test_order_total_price(self):
        self.assertEqual(self.order.total_price, 160.00)

    def test_orderitem_str_and_relation(self):
        self.assertIn('Order Product', str(self.order_item))
        self.assertIn('2', str(self.order_item))
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)

    def test_orderitem_total_price(self):
        self.assertEqual(self.order_item.total_price, 160.00)

    def test_complete_order_and_stock_update(self):
        self.order.complete_order()
        self.order.refresh_from_db()
        self.product.refresh_from_db()
        self.assertEqual(self.order.status, 'completed')
        self.assertEqual(self.product.stock, 13)  # 15 - 2

    def test_complete_order_not_enough_stock(self):
        self.order_item.quantity = 20
        self.order_item.save()
        with self.assertRaises(ValueError):
            self.order.complete_order()

class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='payuser', password='testpass')
        self.product = Product.objects.create(
            name='Pay Product',
            description='For payment test',
            price=120.00,
            stock=8,
            category='fashion',
            seller=self.user
        )
        self.order = Order.objects.create(user=self.user)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=1, price=120.00)
        self.payment = Payment.objects.create(order=self.order, amount=120.00, paid=True, transaction_id='TX123')

    def test_payment_str(self):
        self.assertIn('Order', str(self.payment))
        self.assertIn('Paid', str(self.payment))
        self.assertEqual(self.payment.amount, 120.00)
        self.assertTrue(self.payment.paid)

    def test_payment_not_paid(self):
        order2 = Order.objects.create(user=self.user)
        payment2 = Payment.objects.create(
            order=order2,
            amount=120.00,
            paid=False,
            transaction_id='TX999'
        )
        self.assertFalse(payment2.paid)
        self.assertEqual(payment2.amount, 120.00)
        self.assertIn('TX999', payment2.transaction_id)
        self.assertIn('Order', str(payment2))
        self.assertIn('Not Paid', str(payment2))
