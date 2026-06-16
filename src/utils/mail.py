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
            "email": "vishalsingh37040@gmail.com" # Apna verified Brevo email daalna
        },
        "to": [{"email": email} for email in emails],
        "subject": "Registration Confirmation",
        "htmlContent": "<p>Hi, thanks for Registration in our application. Our team will connect with you shortly!.. </p>"
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