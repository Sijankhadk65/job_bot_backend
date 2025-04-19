import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from email_utils import send_bulk_emails

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def fake_attachments(tmp_path):
    paths = []
    for name in ["cv.pdf", "cover_letter.pdf", "reference_letter.pdf"]:
        path = tmp_path / name
        with open(path, "wb") as f:
            f.write(b"%PDF-1.4 dummy content\n%%EOF")
        paths.append(str(path))
    return paths


@patch("smtplib.SMTP")
def test_send_bulk_emails_with_mongodb(mock_smtp, fake_attachments):

    # Mock SMTP server
    instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = instance

    results = send_bulk_emails(
        sender="me@example.com",
        password="mypassword",
        subject="Hello!",
        body="Dear {name}, welcome to {company}.",
        attachment_paths=fake_attachments,
    )

    assert len(results) == 24
