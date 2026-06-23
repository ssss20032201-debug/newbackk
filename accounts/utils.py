import random
import string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def generate_otp(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))


def send_reset_code(email: str, code: str) -> None:
    subject = f'{code} — FamilyApp kirish kodi'

    digits = ''.join(
        f'<td align="center" style="width:44px;height:54px;background:#f0f7ff;'
        f'border:2px solid #1a73e8;border-radius:10px;margin:0 4px;">'
        f'<span style="font-size:28px;font-weight:900;color:#1a73e8;font-family:Courier,monospace;">{d}</span>'
        f'</td><td style="width:6px;"></td>'
        for d in code
    )

    html = f"""<!DOCTYPE html>
<html lang="uz">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#f4f6f8;font-family:Arial,Helvetica,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:40px 16px;">
<table width="480" cellpadding="0" cellspacing="0"
       style="background:#ffffff;border-radius:16px;border:1px solid #e2e8f0;overflow:hidden;">

  <tr><td style="background:linear-gradient(135deg,#1a73e8,#0d47a1);padding:32px 40px;text-align:center;">
    <span style="font-size:26px;font-weight:900;color:#ffffff;letter-spacing:1px;">FamilyApp</span><br>
    <span style="font-size:13px;color:#bbdefb;letter-spacing:2px;">FAMILY CONTROL</span>
  </td></tr>

  <tr><td style="padding:36px 40px 8px;text-align:center;">
    <h2 style="margin:0 0 8px;font-size:24px;font-weight:800;color:#1a202c;">Kirish kodi</h2>
    <p style="margin:0;font-size:15px;color:#718096;line-height:1.6;">
      Quyidagi kodni ilovaga kiriting
    </p>
  </td></tr>

  <tr><td align="center" style="padding:28px 40px;">
    <table cellpadding="0" cellspacing="0" border="0">
      <tr>{digits}</tr>
    </table>
  </td></tr>

  <tr><td align="center" style="padding:0 40px 12px;">
    <table cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td style="background:#fff8e1;border-radius:8px;padding:10px 20px;border-left:4px solid #f6ad55;">
          <span style="font-size:13px;color:#744210;">Kod <strong>10 daqiqa</strong> amal qiladi</span>
        </td>
      </tr>
    </table>
  </td></tr>

  <tr><td style="padding:20px 40px 32px;border-top:1px solid #e2e8f0;text-align:center;">
    <p style="margin:0;font-size:12px;color:#a0aec0;line-height:1.8;">
      Bu so'rovni siz yubormagan bo'lsangiz, xabarni o'chiring.<br>
      &copy; 2026 FamilyApp
    </p>
  </td></tr>

</table>
</td></tr></table>
</body></html>"""

    text_content = f'FamilyApp kirish kodi: {code}\n10 daqiqa amal qiladi.'

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=f'FamilyApp <{settings.DEFAULT_FROM_EMAIL}>',
        to=[email],
    )
    msg.attach_alternative(html, "text/html")
    try:
        msg.send(fail_silently=False)
    except Exception as e:
        # Log the error but don't crash the server
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Email yuborishda xato ({email}): {e}")
        raise  # re-raise so the view can return 500 with a proper JSON response
