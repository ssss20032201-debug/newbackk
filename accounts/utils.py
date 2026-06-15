import random
import string
from django.core.mail import send_mail
from django.conf import settings


def generate_otp(length: int = 6) -> str:
    """6 raqamli tasodifiy kod"""
    return ''.join(random.choices(string.digits, k=length))


def send_reset_code(email: str, code: str) -> None:
    """Parol tiklash kodini emailga yuborish"""
    send_mail(
        subject='Parolni tiklash kodi — FamilyApp',
        message=f'Sizning parolni tiklash kodingiz: {code}\n\nKod 10 daqiqa davomida amal qiladi.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
