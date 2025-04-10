import pandas as pd
import smtplib
import csv
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv

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
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    # Replace placeholders in the body (e.g., {name}, {company})
    personalized_body = (
        body.replace("{company}", company)
        .replace("{street}", street)
        .replace("{postalCode}", postalCode)
        .replace("{city}", city)
    )
    msg.set_content(personalized_body)

    for filepath in attachments:
        try:
            with open(filepath, "rb") as f:
                file_data = f.read()
                filename = Path(filepath).name
                msg.add_attachment(
                    file_data, maintype="application", subtype="pdf", filename=filename
                )
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
):
    df = pd.read_excel("data/applications.xlsx")

    for _, row in df.iterrows():
        email = row["email"]
        company = row["CompanyName1"] + row["CompanyName2"] + row["CompanyName3"]
        street = row["Street"]
        postalCode = row["PostalCode"]
        city = row["City"]

        if email != "":
            status = send_email(
                sender=sender,
                password=password,
                subject=subject,
                body=body,
                recipient=email,
                company=company,
                attachments=attachment_paths,
                street=street,
                postalCode=postalCode,
                city=city,
            )
            status_str = "sent" if status else "failed"
        else:
            print(f"❌ Failed to send to {company}: No email available")
            status_str = "No email"
        log_email_result("", company, status_str)
