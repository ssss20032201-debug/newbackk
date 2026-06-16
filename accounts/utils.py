import random
import string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def generate_otp(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))


def _base_email(title: str, body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{title}</title>
</head>
<body style="margin:0;padding:0;background:#f4f6f8;font-family:Arial,Helvetica,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0">
    <tr>
      <td align="center" style="padding:40px 16px;">
        <table width="500" cellpadding="0" cellspacing="0" border="0"
               style="background:#ffffff;border-radius:12px;border:1px solid #e2e8f0;overflow:hidden;">

          <!-- Top bar -->
          <tr>
            <td style="background:#1a73e8;padding:6px 0;"></td>
          </tr>

          <!-- Logo -->
          <tr>
            <td align="center" style="padding:32px 40px 16px;">
              <span style="font-size:22px;font-weight:800;color:#1a73e8;letter-spacing:0.5px;">FamilyApp</span>
            </td>
          </tr>

          <!-- Body -->
          {body_html}

          <!-- Footer -->
          <tr>
            <td align="center" style="padding:24px 40px 32px;border-top:1px solid #e2e8f0;">
              <p style="margin:0;font-size:12px;color:#a0aec0;line-height:1.6;">
                Bu xabar avtomatik yuborildi. Javob bermang.<br>
                &copy; 2026 FamilyApp
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def send_welcome_email(email: str, full_name: str) -> None:
    subject = f'FamilyApp ga xush kelibsiz, {full_name}!'
    first_name = full_name.split()[0]

    body_html = f"""
          <tr>
            <td style="padding:8px 40px 32px;">
              <h2 style="margin:0 0 12px;font-size:22px;color:#1a202c;">
                Salom, {first_name}!
              </h2>
              <p style="margin:0 0 16px;font-size:15px;color:#4a5568;line-height:1.6;">
                FamilyApp ga ro'yxatdan o'tganingiz uchun rahmat.
                Oilangiz bilan bog'liq barcha narsalarni bir joyda boshqaring.
              </p>
              <table cellpadding="0" cellspacing="0" border="0" style="margin:24px 0;">
                <tr>
                  <td style="background:#f7fafc;border-radius:8px;border:1px solid #e2e8f0;padding:16px 20px;">
                    <p style="margin:0 0 8px;font-size:13px;font-weight:700;color:#2d3748;text-transform:uppercase;letter-spacing:0.5px;">Nima qila olasiz:</p>
                    <p style="margin:4px 0;font-size:14px;color:#4a5568;">Farzandlar joylashuvini kuzatish</p>
                    <p style="margin:4px 0;font-size:14px;color:#4a5568;">Vazifalar va mukofotlar berish</p>
                    <p style="margin:4px 0;font-size:14px;color:#4a5568;">Oila a'zolari bilan hamkorlik</p>
                  </td>
                </tr>
              </table>
              <p style="margin:0;font-size:14px;color:#718096;">
                Savollaringiz bo'lsa, doimo yordam berishga tayyormiz.
              </p>
            </td>
          </tr>"""

    text_content = f"Salom {full_name}, FamilyApp ga xush kelibsiz!"

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    msg.attach_alternative(_base_email(subject, body_html), "text/html")
    msg.send(fail_silently=True)


def send_reset_code(email: str, code: str) -> None:
    subject = 'FamilyApp — Tasdiqlash kodi'

    body_html = f"""
          <tr>
            <td style="padding:8px 40px 32px;">
              <h2 style="margin:0 0 12px;font-size:22px;color:#1a202c;">Tasdiqlash kodi</h2>
              <p style="margin:0 0 24px;font-size:15px;color:#4a5568;line-height:1.6;">
                Parolni yangilash uchun quyidagi kodni ilovaga kiriting.
              </p>
              <table cellpadding="0" cellspacing="0" border="0" align="center" style="margin:0 auto 24px;">
                <tr>
                  <td align="center"
                      style="background:#1a73e8;border-radius:10px;padding:18px 40px;">
                    <span style="font-size:36px;font-weight:900;color:#ffffff;letter-spacing:10px;font-family:Courier,monospace;">{code}</span>
                  </td>
                </tr>
              </table>
              <p style="margin:0;font-size:13px;color:#a0aec0;text-align:center;">
                Kod 10 daqiqa davomida amal qiladi.<br>
                Agar siz bu so'rov yubormagan bo'lsangiz, xabarni e'tiborsiz qoldiring.
              </p>
            </td>
          </tr>"""

    text_content = f'Tasdiqlash kodingiz: {code}\nKod 10 daqiqa davomida amal qiladi.'

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    msg.attach_alternative(_base_email(subject, body_html), "text/html")
    msg.send(fail_silently=False)
