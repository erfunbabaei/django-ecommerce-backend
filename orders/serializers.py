from rest_framework import serializers
from .models import Cart, Order, Payment, OrderItem
from products.serializers import ProductSerializer

# ----------------------------
# Cart
# ----------------------------

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity']

# ----------------------------
# Order
# ----------------------------

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orders_items', many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'status', 'created_at', 'total_price']

    def get_total_price(self, obj):
        total = sum([item.product.price * item.quantity for item in obj.order_items.all()])
        return total

# ----------------------------
# Payment
# ----------------------------

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'paid', 'payment_date', 'transaction_id']
        read_only_fields = ['paid', 'payment_date', 'transaction_id']
