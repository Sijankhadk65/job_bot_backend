from celery_worker import celery_app
from email_utils import send_bulk_emails


@celery_app.task
def test_task(name: str):
    print(f"Hello from the task to {name}")


# @celery_app.task
# def send_bulk_email_task(
#     sender,
#     password,
#     subject,
#     body,
#     attachment_paths,
# ):
#     send_bulk_emails(
#         sender=sender,
#         password=password,
#         subject=subject,
#         body=body,
#         attachment_paths=attachment_paths,
#     )
