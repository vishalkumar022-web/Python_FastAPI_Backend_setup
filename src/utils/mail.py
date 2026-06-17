import httpx
from typing import List
from src.utils.settings import settings

async def send_email(emails: List[str]):
    # Brevo API ka endpoint URL
    url = "https://api.brevo.com/v3/smtp/email"

    # API call ke liye zaroori headers (yahan tumhari API key jayegi)
    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }

    # Email ka content aur details
    payload = {
        "sender": {
            "name": "Task Management Application",
            "email": "vishalsingh37040@gmail.com"
        },
        "replyTo": {
            "email": "vishalsingh37040@gmail.com",
            "name": "Vishal Support"
        },
        "to": [{"email": email} for email in emails],
        "subject": "Registration Confirmation - Welcome!",
        "htmlContent": """
        <html>
            <body>
                <h2>Welcome to Task Management!</h2>
                <p>Hi there,</p>
                <p>Thanks for successfully registering in our application. We are thrilled to have you on board!</p>
                <p>Our team will connect with you shortly. If you have any questions, just reply to this email.</p>
                <br>
                <p>Best Regards,<br><b>Vishal's Task App Team</b></p>
            </body>
        </html>
        """
    }

    try:
        # httpx ka use karke async API call
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            
            # Agar response 201 (Created) aata hai toh email successful hai
            if response.status_code == 201:
                print("✅ Brevo API se Email successfully background me chala gaya!")
            else:
                print(f"❌ Brevo API Error: {response.status_code} - {response.text}")
                
    except Exception as e:
        print(f"❌ Bhai, Email API call me error aaya: {e}")