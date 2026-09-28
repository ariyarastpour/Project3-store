from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
)

app_name = 'accounts-api-v1'

urlpatterns = [
    # ─── Registration ───
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),

    # ─── Activation ───
    path(
        'activation/confirm/<uuid:token>/',
        views.ActivationView.as_view(),
        name='activation-confirm'
    ),
    path(
        'activation/code/',
        views.ActivationCodeView.as_view(),
        name='activation-code'
    ),
    path(
        'activation/resend/',
        views.ResendActivationView.as_view(),
        name='activation-resend'
    ),

    # ─── Change password ───
    path(
        'change-password/',
        views.ChangePasswordApiView.as_view(),
        name='change-password'
    ),

    # ─── Reset password ───
    path('reset_password/', views.PasswordResetRequestApiView.as_view(), name='reset-password'),
    path('reset_password/confirm/', views.PasswordResetConfirmApiView.as_view(), name='reset-password-confirm'),

    # ─── Token login ───
    path('token/login/', views.CustomAuthToken.as_view(), name='token-login'),
    path('token/logout/', views.CustomDiscardAuthToken.as_view(), name='token-logout'),

    # ─── JWT ───
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),

    # ─── Profile ───
    path('profile/', views.ProfileApiView.as_view(), name='profile'),
]