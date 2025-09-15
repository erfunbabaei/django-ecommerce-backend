from orders.models import Order, OrderItem
from products.models import Product
from rest_framework import generics, permissions
from products.serializers import ProductSerializer
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from orders.serializers import OrderSerializer
from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

# ----------------------------
# Sales Report
# ----------------------------

class SalesReportAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        completed_orders = Order.objects.filter(status='completed')

        if start_date:
            completed_orders = completed_orders.filter(created_at__gte=start_date)
        if end_date:
            completed_orders = completed_orders.filter(created_at__lte=end_date)

        total_sales = completed_orders.count()
        total_revenue = sum(
            sum(item.price * item.quantity for item in order.order_items.all())
            for order in completed_orders
        )
        orders_data = []
        product_stats = defaultdict(lambda: {'quantity_sold': 0, 'revenue': 0})

        for order in completed_orders:
            items = OrderItem.objects.filter(order=order)
            items_data = []

            for item in items:
                items_data.append({
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                    'price': item.price,
                })

                product_stats[item.product.name]['quantity_sold'] += item.quantity
                product_stats[item.product.name]['revenue'] += item.price * item.quantity

            orders_data.append({
                'id': order.id,
                'user': order.user.username,
                'total_price': order.total_price,
                'status': order.status,
                'created_at': order.created_at,
                'items': items_data
            })

        top_products_by_quantity = sorted(
            product_stats.items(),
            key=lambda x: x[1]['quantity_sold'],
            reverse=True
        )

        top_products_by_revenue = sorted(
            product_stats.items(),
            key=lambda x: x[1]['revenue'],
            reverse=True
        )

        data = {
            'total_sales': total_sales,
            'total_revenue': total_revenue,
            'orders': orders_data,
            'top_products_by_quantity': top_products_by_quantity,
            'top_products_by_revenue': top_products_by_revenue,
        }

        return Response(data)

# ----------------------------
# Allow Admins Manage Products
# ----------------------------

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

# ----------------------------
# Allow Admins Manage Users
# ----------------------------

class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]

# ----------------------------
# Allow Admins Manage Orders
# ----------------------------

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

class OrderRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]
