from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import update_last_login
from rest_framework import generics, permissions
from .serializers import UserProfileSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from .serializers import PasswordResetSerializer

# ----------------------------
# Register API / View
# ----------------------------
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        username = request.data.get('username')
        email = request.data.get('email')
        phone = request.data.get('phone')
        address = request.data.get('address')
        password = request.data.get('password')

        if not first_name:
            return Response({"error": "First name required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not last_name:
            return Response({"error": "Last name required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not username:
            return Response({"error": "Username required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not email:
            return Response({"error": "Email required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({"error": "Password required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(phone=phone).exists():
            return Response({"error": "Phone already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            first_name=first_name,
            last_name = last_name,
            username=username,
            email=email,
            phone=phone,
            address=address,
            password=password
        )

        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)

# ----------------------------
# Custom JWT Login (sets cookies)
# ----------------------------
class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            tokens = response.data

            username_or_email = request.data.get("username") or request.data.get("email")
            user = User.objects.filter(username=username_or_email).first() or \
                   User.objects.filter(email=username_or_email).first()

            if user:
                update_last_login(None, user)

            response.set_cookie(
                key="access_token",
                value=tokens["access"],
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=3600
            )
            response.set_cookie(
                key="refresh_token",
                value=tokens["refresh"],
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=7 * 24 * 3600
            )

        return response

# ----------------------------
# Logout API / View
# ----------------------------
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = JsonResponse({"message": "Logged out successfully"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.status_code = 302
        response["Location"] = ""
        return response

# ----------------------------
# User Profile / View
# ----------------------------

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# ----------------------------
# Reset Password
# ----------------------------

class PasswordResetView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Email does not exist."}, status=status.HTTP_200_OK)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://localhost:8000/reset/{uid}/{token}/"

        send_mail(
            "Password Reset",
            f"Open this link to change your password.: {reset_link}",
            "from@example.com",
            [email],
            fail_silently=False,
        )

        return Response({"detail": "A password change link has been sent to your email."},
                        status=status.HTTP_200_OK)

