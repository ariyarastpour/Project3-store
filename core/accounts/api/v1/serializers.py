from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from ...models import Profile, PasswordResetToken
from accounts.models import ActivationToken

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def validate_email(self, value):
        value = value.lower().strip()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("این ایمیل قبلاً ثبت شده است."))
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        confirm = attrs.get('confirm_password')

        if password != confirm:
            raise serializers.ValidationError(
                {'confirm_password': _("رمز عبور و تکرار آن یکسان نیستند.")}
            )

        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        return attrs

    def create(self, validated_data):
        """ساخت کاربر"""
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False,
            is_verified=False,
        )
        return user
    

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_verified:
                raise serializers.ValidationError({"details": "user is not verified"})
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"details": "user is not verified"})
        validated_data['email'] = self.user.email
        validated_data['user_id'] = self.user.id
        return validated_data
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get('new_password1') != attrs.get('new_password2'):
            raise serializers.ValidationError({"details": "passwords dosnt match"})
        
        try:
            validate_password(attrs.get("new_password1"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'email', 'first_name', 'last_name', 'image', 'description']



class ActivationSerializer(serializers.Serializer):
    token = serializers.UUIDField()

    def validate_token(self, value):
        try:
            token_obj = ActivationToken.objects.select_related('user').get(token=value)
        except ActivationToken.DoesNotExist:
            raise serializers.ValidationError("لینک نامعتبر است.")

        if token_obj.is_expired():
            token_obj.delete()
            raise serializers.ValidationError("لینک منقضی شده است.")

        if token_obj.user.is_verified:
            raise serializers.ValidationError("حساب قبلاً فعال شده است.")

        self.context['token_obj'] = token_obj
        return value


class ActivationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)

    def validate(self, attrs):
        email = attrs['email'].lower().strip()
        code = attrs['code']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "کاربری با این ایمیل وجود ندارد."}
            )

        token_obj = ActivationToken.objects.filter(user=user, otp_code=code).first()
        if not token_obj:
            raise serializers.ValidationError({"code": "کد وارد شده صحیح نیست."})

        if token_obj.is_expired():
            token_obj.delete()
            raise serializers.ValidationError({"code": "کد منقضی شده است."})

        if user.is_verified:
            raise serializers.ValidationError({"detail": "حساب قبلاً فعال شده است."})

        attrs['token_obj'] = token_obj
        return attrs


class ResendActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        return value.lower().strip()

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        return value.lower().strip()


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    token = serializers.UUIDField(required=False)
    code = serializers.CharField(max_length=6, min_length=6, required=False)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        token = attrs.get('token')
        code = attrs.get('code')

        if not token and not code:
            raise serializers.ValidationError(
                {"detail": "یکی از فیلدهای token یا code الزامی است."}
            )

        try:
            if token:
                token_obj = PasswordResetToken.objects.select_related('user').get(token=token)
            else:
                email = attrs.get('email')
                if not email:
                    raise serializers.ValidationError(
                        {"email": "برای استفاده از کد، ایمیل الزامی است."}
                    )
                token_obj = PasswordResetToken.objects.select_related('user').filter(
                    user__email=email.lower().strip(),
                    otp_code=code,
                ).first()
                if not token_obj:
                    raise serializers.ValidationError({"code": "کد وارد شده صحیح نیست."})
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({"token": "لینک نامعتبر است."})

        if token_obj.is_expired():
            token_obj.delete()
            raise serializers.ValidationError(
                {"detail": "لینک/کد منقضی شده است. لطفاً دوباره درخواست دهید."}
            )

        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"confirm_password": "رمز عبور و تکرار آن یکسان نیستند."}
            )

        attrs['token_obj'] = token_obj
        return attrs