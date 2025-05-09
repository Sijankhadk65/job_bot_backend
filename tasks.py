from celery_worker import celery_app
from email_utils import send_bulk_emails
from database.database import *
from config.config import initiate_database
from beanie.operators import In


@celery_app.task
def test_task(name: str):
    print(f"Hello from the task to {name}")


@celery_app.task
def send_batched_emails(
    sender, password, subject, body, attachment_paths, categories, regions
):
    import asyncio

    async def main():
        await initiate_database()

        print("In the task's async function")

        print("Fetching Code from Categories...")
        codes = set()
        companies = []

        for category in categories:
            category_codes = await retrive_category_codes(category)
            codes.update(category_codes)

        print("Fetching Companies from the Regions...")
        companies = await retrive_coded_companies(In("location.bundesland", regions))
        print(f"A total of {len(companies)} found in the regions")

        companies = [
            c.model_dump(exclude={"id", "_id"})
            for c in companies
            if any(code in codes for code in c.branchCodes)
        ]

        print(f"A total of {len(companies)} in the regions match the categories")

        print("Sending mails in batches...")

        batch_size = 500
        for i in range(0, len(companies), batch_size):
            batch = companies[i : i + batch_size]
            print(f"Sending emails for {i} batch...")
            send_email_batch.delay(
                sender=sender,
                password=password,
                subject=subject,
                body=body,
                attachment_paths=attachment_paths,
                batch=batch,
            )

    asyncio.run(main())


@celery_app.task(bind=True, max_retries=3)
def send_email_batch(self, *, sender, password, subject, body, attachment_paths, batch):
    from email_utils import send_email

    print("Mail Sent...")

    for company in batch:
        send_email(
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


@celery_app.task
def send_bulk_email_task(
    sender,
    password,
    subject,
    body,
    attachment_paths,
    companies,
):
    send_bulk_emails(
        sender=sender,
        password=password,
        subject=subject,
        body=body,
        attachment_paths=attachment_paths,
        companies=companies,
    )
