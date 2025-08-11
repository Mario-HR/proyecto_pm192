from fastapi_mail import FastMail, MessageSchema
from mail.config import conf

async def send_email(email_to: str, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
