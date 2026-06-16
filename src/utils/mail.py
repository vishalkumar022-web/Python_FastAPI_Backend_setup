from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from typing import List
from src.utils.settings import settings

conf = ConnectionConfig(
    MAIL_USERNAME = "vishalsingh37040@gmail.com",
    MAIL_PASSWORD = settings.APP_PASSWORD, 
    MAIL_FROM = "vishalsingh37040@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Task_Management Application",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_email(emails: List[str]):
    try:
        html = """<p>Hi, thanks for Registration in our application. Our team will connect with you shortly!.. </p> """

        message = MessageSchema(
            subject="Registration Confirmation",
            recipients=emails,
            body=html,
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message)
        print("✅ Email successfully background me chala gaya!")
        
    except Exception as e:
        # Agar koi SMTP ya connection error aayega, toh server crash nahi hoga, 
        # bas terminal me ye message print ho jayega.
        print(f"❌ Bhai, Email bhejne me error aaya: {e}")