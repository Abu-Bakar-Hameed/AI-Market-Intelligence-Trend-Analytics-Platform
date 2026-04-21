import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_USER, EMAIL_PASS

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(to_email: str, subject: str, body: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

    except smtplib.SMTPAuthenticationError:
        print("❌ Gmail authentication failed. Use App Password.")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")


def send_otp_email(email: str, otp: str):
    subject = "OTP Verification"
    body = f"""
    <h2>Your OTP Code</h2>
    <p><b>{otp}</b></p>
    """
    send_email(email, subject, body)


def send_reset_email(email: str, token: str):
    reset_link = f"http://localhost:8000/reset-password?token={token}"

    subject = "Reset Your Password"
    body = f"""
    <h2>Password Reset Request</h2>
    <p>Click the link below to reset your password:</p>
    <a href="{reset_link}">{reset_link}</a>
    """

    send_email(email, subject, body)