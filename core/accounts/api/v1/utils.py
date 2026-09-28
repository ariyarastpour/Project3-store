import threading
from mail_templated import EmailMessage


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        try:
            self.email.send()
        except Exception as e:
            print(f"[EmailThread] خطا: {e}")


def send_activation_email(user, token_obj, request):
    activation_link = request.build_absolute_uri(
        f"/accounts/api/v1/activation/confirm/{token_obj.token}/"
    )

    email = EmailMessage(
        'accounts/email/activation.tpl',
        {
            'email': user.email,
            'link': activation_link,
            'code': token_obj.otp_code,
            'expires_hours': 24,
        },
        'Front@shop.com',
        [user.email],
    )

    EmailThread(email).start()