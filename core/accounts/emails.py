from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


def send_password_reset_email(user, token_obj, request):

    reset_path = reverse(
        'accounts-api-v1:password-reset-confirm',
    )

    reset_link = request.build_absolute_uri(
        f"{reset_path}?token={token_obj.token}"
    )

    subject = 'بازنشانی رمز عبور'
    message = f"""
درود،

برای بازنشانی رمز عبور خود از لینک زیر استفاده کنید:
{reset_link}

یا کد زیر را در اپلیکیشن وارد کنید:
{token_obj.otp_code}

این کد/لینک تا ۱۵ دقیقه اعتبار دارد.

اگر شما این درخواست را نداده‌اید، این ایمیل را نادیده بگیرید.

با تشکر
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )