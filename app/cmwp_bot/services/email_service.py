from aiosmtplib import send
from email.message import EmailMessage

from app.cmwp_bot.settings import config


async def send_plan_email(full_name: str, username_link: str, phone: str, company: str, answers_text: str) -> None:
    msg = EmailMessage()
    msg["From"] = config.SMTP_USER
    msg["To"] = config.EMAIL_ADRESS
    msg["Subject"] = f"Запрос плана от {full_name}"

    html = f"""
    <h3>📥 Запрос плана</h3>
    <p><b>Имя:</b> {full_name}<br>
    <b>Телефон:</b> {phone or "—"}<br>
    <b>Компания:</b> {company or "—"}<br>
    <b>Профиль:</b> <a href="{username_link}">{username_link}</a></p>
    <hr>
    <h4>📋 Ответы на анкету:</h4>
    <pre>{answers_text}</pre>
    """

    msg.set_content("Письмо содержит HTML-формат.")
    msg.add_alternative(html, subtype="html")

    await send(
        msg,
        hostname="smtp.gmail.com",
        port=587,
        username=config.SMTP_USER,
        password=config.SMTP_PASS,
        start_tls=True,
    )


async def send_discuss_email(full_name: str, username_link: str, phone: str, company: str):
    msg = EmailMessage()
    msg['From'] = config.SMTP_USER
    msg['To'] = config.EMAIL_ADRESS
    msg['Subject'] = f'Запрос обсуждения проекта — {full_name}'

    msg.set_content(
        f'Пользователь хочет обсудить проект:\n\n'
        f'Имя: {full_name}\n'
        f'Компания: {company}\n'
        f'Телефон: {phone}\n'
        f'Профиль: {username_link}\n'
    )

    await send(
        msg,
        hostname='smtp.gmail.com',
        port=587,
        username=config.SMTP_USER,
        password=config.SMTP_PASS,
        start_tls=True,
    )