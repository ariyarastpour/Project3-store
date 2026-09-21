from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenObtainPairView, 
    TokenRefreshView,
)

app_name = 'accounts-api-v1'


urlpatterns = [
    # Registration
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),

    # Change password
    path('change-password/', views.ChangwPasswordApiView.as_view(), name='registration'),

    # Login token
    path('token/login/', views.CustomAuthToken.as_view(), name='token-login'),
    path('token/logout/', views.CustomDiscardAuthToken.as_view(), name='token-logout'),

    # Login jwt
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),

    # Profile
    path('profile/', views.ProfileApiView.as_view(), name='profile'),

    # test email
    path('activation/test', views.TestEmailView.as_view(), name='test-activation-email')
]


