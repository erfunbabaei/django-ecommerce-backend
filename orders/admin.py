from django.contrib import admin
from .models import Order, Payment

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'get_total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'id')

    def get_total_price(self, obj):
        return obj.total_price
    get_total_price.short_description = 'Total Price'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'paid', 'transaction_id')
    list_filter = ('paid',)
    search_fields = ('order__id', 'transaction_id')
