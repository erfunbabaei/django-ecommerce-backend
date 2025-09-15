from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active', 'is_seller', 'is_admin_sub')
    search_fields = ('email', 'username')
    list_filter = ('is_staff', 'is_seller', 'is_active')
