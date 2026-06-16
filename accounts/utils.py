import random
import string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def generate_otp(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))


def send_reset_code(email: str, code: str) -> None:
    subject = 'Parolni tiklash kodi — FamilyApp'

    text_content = f'Sizning parolni tiklash kodingiz: {code}\nKod 10 daqiqa davomida amal qiladi.'

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background-color:#f0f4f8;font-family:Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0f4f8;padding:40px 0;">
    <tr>
      <td align="center">
        <table width="480" cellpadding="0" cellspacing="0" style="background-color:#e8f4fd;border-radius:16px;overflow:hidden;">

          <!-- Header -->
          <tr>
            <td align="center" style="padding:36px 40px 20px;">
              <div style="width:60px;height:60px;background-color:#1a73e8;border-radius:50%;display:inline-block;text-align:center;line-height:60px;">
                <span style="font-size:28px;">👨‍👩‍👧</span>
              </div>
              <br><br>
              <span style="color:#1a73e8;font-size:20px;font-weight:bold;letter-spacing:1px;">FamilyApp</span>
            </td>
          </tr>

          <!-- Title -->
          <tr>
            <td align="center" style="padding:0 40px 12px;">
              <h1 style="margin:0;font-size:26px;font-weight:800;color:#1a202c;">Parolni tiklash</h1>
              <p style="margin:10px 0 0;font-size:15px;color:#4a5568;">Quyidagi kodni ilovaga kiriting</p>
            </td>
          </tr>

          <!-- OTP Code -->
          <tr>
            <td align="center" style="padding:24px 40px;">
              <div style="background-color:#1a73e8;border-radius:14px;padding:20px 48px;display:inline-block;">
                <span style="font-size:42px;font-weight:900;color:#ffffff;letter-spacing:12px;">{code}</span>
              </div>
            </td>
          </tr>

          <!-- Timer note -->
          <tr>
            <td align="center" style="padding:0 40px 16px;">
              <p style="margin:0;font-size:13px;color:#718096;">⏱ Kod <strong>10 daqiqa</strong> davomida amal qiladi</p>
            </td>
          </tr>

          <!-- Divider -->
          <tr>
            <td style="padding:0 40px;">
              <hr style="border:none;border-top:1px solid #bee3f8;margin:0;">
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td align="center" style="padding:20px 40px 32px;">
              <p style="margin:0;font-size:12px;color:#a0aec0;">
                Agar siz bu so'rovni yubormagan bo'lsangiz, ushbu xabarni e'tiborsiz qoldiring.<br><br>
                © 2026 FamilyApp
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
