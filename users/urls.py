from django.urls import path
from .views import CustomLoginView, LogoutAPIView, RegisterAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserProfileView
from .views import PasswordResetView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register_api'),
    path('login/', CustomLoginView.as_view(), name='login_api'),  # JWT login
    path('logout/', LogoutAPIView.as_view(), name='logout_api'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh token
    path("me/", UserProfileView.as_view(), name="user-profile"),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
]