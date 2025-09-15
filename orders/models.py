from typing import Any
from django.db import models
from django.conf import settings
from products.models import Product
from users.models import CustomUser

# ----------------------------
# Cart
# ----------------------------

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"

# ----------------------------
# Order
# ----------------------------

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "pending"),
        ("shipped", "shipped"),
        ("completed", "completed"),
        ("canceled", "canceled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def complete_order(self):
        if self.status == 'completed':
            return
        for item in self.order_items.all():
            product = item.product
            if item.quantity > product.stock:
                raise ValueError(f"Not enough stock for {product.name}")
        for item in self.order_items.all():
            product = item.product
            product.stock -= item.quantity
            product.save()
        self.status = 'completed'
        self.save()

    @property
    def total_price(self):
        return sum(item.price * item.quantity for item in self.order_items.all())

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

# ----------------------------
# Payment
# ----------------------------

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        status = "Paid" if self.paid else "Not Paid"
        return f"Payment for Order {self.order.id} - {status}"


