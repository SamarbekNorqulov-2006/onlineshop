from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(to_email, code):
    subject = "Tasdiqlash kodi"
    message = f"Sizning tasdiqlash kodingiz: {code}"
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(
        subject,
        message,
        from_email,
        [to_email],
        fail_silently=False
    )