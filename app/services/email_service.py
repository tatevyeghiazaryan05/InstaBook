import time
import smtplib
from email.message import EmailMessage
import secrets
import string


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "tatevikyeghiazaryann5@gmail.com"
EMAIL_PASSWORD = "klcm ecsh nfcb xhzs"


def generate_verification_code(length=8):
    characters = string.ascii_letters + string.digits
    random_part = ''.join(secrets.choice(characters) for _ in range(length))
    timestamp_part = str(int(time.time() * 1000))
    return random_part + timestamp_part


def send_verification_email(user_email, code):
    """Send verification code to user email"""

    msg = EmailMessage()
    msg["Subject"] = "Click here "
    msg["From"] = EMAIL_SENDER
    msg["To"] = user_email
    msg.set_content(f"{code}")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception:
        print("Error sending email:")
        return False
