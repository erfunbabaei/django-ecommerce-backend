from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, OrderViewSet, OrderStatusUpdateAPIView, FakePaymentAPIView


router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
    path('orders/<int:pk>/update_status/', OrderStatusUpdateAPIView.as_view(), name='order-update-status'),
    path('payment/<int:order_id>/', FakePaymentAPIView.as_view(), name='fake-payment'),

]
