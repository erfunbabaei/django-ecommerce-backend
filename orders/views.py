from .serializers import CartSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Order, Cart, Payment, OrderItem
from .serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
import uuid
from .serializers import PaymentSerializer



# ----------------------------
# Order / View
# ----------------------------

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ----------------------------
# Order / View
# ----------------------------

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"detail": "The shopping cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=user)

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        order.complete_order()

        cart_items.delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderStatusUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get("status")
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "The status is not valid."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ----------------------------
# Payment
# ----------------------------

class FakePaymentAPIView(APIView):
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if hasattr(order, 'payment'):
            return Response({"error": "Payment already exists"}, status=status.HTTP_400_BAD_REQUEST)


        payment = Payment.objects.create(
            order=order,
            amount=order.total_price,
            paid=True,
            transaction_id=str(uuid.uuid4())
        )

        order.status = "completed"
        order.save()

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)