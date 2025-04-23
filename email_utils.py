import smtplib
import csv
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
from dotenv import load_dotenv
from models import Company
from typing import List

load_dotenv()

LOG_FILE = "data/send_log.csv"


def log_email_result(email, company, status):
    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), email, company, status])


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(
    sender,
    password,
    subject,
    body,
    recipient,
    company,
    attachments,
    street,
    postalCode,
    city,
):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    # Replace placeholders in the body (e.g., {name}, {company})
    personalized_body = (
        body.replace("{company}", company).replace("{street}", street)
        # .replace("{postalCode}", str(postalCode))
        .replace("{city}", city)
    )
    msg.attach(MIMEText(personalized_body,"html"))

    for filepath in attachments:
        try:
            with open(filepath, "rb") as f:
                file_data = f.read()
                filename = Path(filepath).name
                part = MIMEApplication(file_data, Name=filename)
                part["Content-Disposition"] = f'attachment; filename="{filename}"'
                msg.attach(part)
        except FileNotFoundError:
            print(f"Failed to attach file {filepath}: {e}")
            return False

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            print(f"✅ Email sent to {recipient}")
            return True
    except Exception as e:
        print(f"❌ Failed to send to {recipient}: {e}")
        return False


def send_bulk_emails(
    sender,
    password,
    subject,
    body,
    attachment_paths,
    companies,
):
    print("🕚 Sending Email To selected Companies...")
    for company in companies:
        if company["contact"]["email"] != None:
            status = send_email(
                sender=sender,
                password=password,
                subject=subject,
                body=body,
                recipient=company["contact"]["email"],
                company=company["companyNames"]["primary"],
                attachments=attachment_paths,
                street=company["address"]["street"],
                postalCode=company["address"]["postalCode"],
                city=company["address"]["city"],
            )
            status_str = "sent" if status else "failed"
        else:
            print(f"❌ Failed to send:  No email available")
            status_str = "No email"
        log_email_result("", company["companyNames"]["primary"], status_str)
