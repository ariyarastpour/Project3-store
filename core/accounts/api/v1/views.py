from rest_framework import status
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ...models import Profile, PasswordResetToken
from .utils import send_activation_email
User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        ActivationToken.objects.filter(user=user).delete()

        token_obj = ActivationToken.objects.create(user=user)
        send_activation_email(user, token_obj, request)

        return Response(
            {
                "detail": "ثبت‌نام انجام شد. لطفاً ایمیل خود را بررسی کنید.",
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response({
            'user_id': user.pk,
            'email': user.email
        })
    

class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data= request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.validated_data.get("old_password")):
                return Response({"old_password" : "Wronge password."}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password1"))
            self.object.save()
            return Response({"details": "password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user= self.request.user)
        return obj


class ActivationView(generics.GenericAPIView):

    serializer_class = ActivationSerializer
    permission_classes = [AllowAny]

    def get(self, request, token, *args, **kwargs):
        serializer = self.get_serializer(data={'token': token})
        serializer.is_valid(raise_exception=True)

        token_obj = serializer.context['token_obj']
        user = token_obj.user

        user.is_verified = True
        user.is_active = True
        user.save(update_fields=['is_verified', 'is_active'])

        token_obj.delete()

        return Response(
            {
                "detail": "حساب شما با موفقیت فعال شد.",
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )


class ActivationCodeView(generics.GenericAPIView):

    serializer_class = ActivationCodeSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token_obj = serializer.validated_data['token_obj']
        user = token_obj.user

        user.is_verified = True
        user.is_active = True
        user.save(update_fields=['is_verified', 'is_active'])

        token_obj.delete()

        return Response(
            {
                "detail": "حساب شما با موفقیت فعال شد.",
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )


class ResendActivationView(generics.GenericAPIView):
    serializer_class = ResendActivationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '').lower().strip()

        generic_response = {
            "detail": "اگر این ایمیل در سیستم ثبت شده باشد، لینک فعال‌سازی ارسال می‌شود."
        }

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(generic_response, status=status.HTTP_200_OK)

        if user.is_verified:
            return Response(
                {"detail": "این حساب قبلاً فعال شده است."},
                status=status.HTTP_200_OK,
            )

        ActivationToken.objects.filter(user=user).delete()
        token_obj = ActivationToken.objects.create(user=user)

        send_activation_email(user, token_obj, request)

        return Response(generic_response, status=status.HTTP_200_OK)
 

# accounts/api/v1/views.py
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.emails import send_password_reset_email
from accounts.models import PasswordResetToken

from .serializers import (
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)

User = get_user_model()


class PasswordResetRequestApiView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        generic_response = {
            "detail": "اگر این ایمیل در سیستم ثبت شده باشد، لینک بازنشانی ارسال می‌شود."
        }

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(generic_response, status=status.HTTP_200_OK)

        PasswordResetToken.objects.filter(user=user).delete()
        token_obj = PasswordResetToken.objects.create(user=user)
        send_password_reset_email(user, token_obj, request)

        return Response(generic_response, status=status.HTTP_200_OK)


class PasswordResetConfirmApiView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token_obj = serializer.validated_data['token_obj']
        user = token_obj.user

        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])
        token_obj.delete()

        return Response(
            {
                "detail": "رمز عبور با موفقیت تغییر کرد.",
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )