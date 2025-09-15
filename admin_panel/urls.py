from django.urls import path
from .views import SalesReportAPIView
from . import views

urlpatterns = [
    path('sales-report/', SalesReportAPIView.as_view(), name='sales_report'),

    # Products
    path('products/', views.ProductListCreateAPIView.as_view(), name='admin-product-list-create'),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDestroyAPIView.as_view(), name='admin-product-detail'),

    # Users
    path('users/', views.UserListAPIView.as_view(), name='admin-user-list'),
    path('users/<int:pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='admin-user-detail'),

    # Orders
    path('orders/', views.OrderListAPIView.as_view(), name='admin-order-list'),
    path('orders/<int:pk>/', views.OrderRetrieveUpdateAPIView.as_view(), name='admin-order-detail'),
]
