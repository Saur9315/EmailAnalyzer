import imaplib
import email
from email.header import decode_header
from decouple import config
from datetime import datetime, timedelta


def get_plain_text_from_email(msg):
    # Initialize an empty list to store plain text parts
    plain_text_parts = []

    # Walk through the email's parts
    for part in msg.walk():
        # Check if the part is plain text
        if part.get_content_type() == "text/plain":
            # Decode the payload and append to the list
            plain_text_parts.append(part.get_payload(decode=True).decode("utf-8"))

    # Join the plain text parts into a single string
    return "\n".join(plain_text_parts)


def get_last_week_date():
    # Calculate the date from one week ago
    last_week_date = datetime.now() - timedelta(weeks=1)
    # Format the date in a way compatible with the IMAP SINCE criterion
    return last_week_date.strftime("%d-%b-%Y")

def get_email_messages(email_address, password):
    # Connect to Gmail's IMAP server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_address, password)

    # Select the mailbox ("inbox")
    mail.select("inbox")

    # Search for all emails in the mailbox
    # status, messages = mail.search(None, "ALL")  # also UNSEEN, f"(UNSEEN SINCE {date})"
    status, messages = mail.search(None, f"(SINCE {get_last_week_date()})")  # also UNSEEN, f"(UNSEEN SINCE {date})"
    message_ids = messages[0].split()

    all_emails = []
    for message_id in message_ids:
        # Fetch the email by its ID
        status, msg_data = mail.fetch(message_id, "(RFC822)")
        raw_email = msg_data[0][1]
        # Parse the raw email using the email library
        msg = email.message_from_bytes(raw_email)
        # Extract info such as sender, subject, and content type
        sender = msg.get("From")
        subject, encoding = decode_header(msg.get("Subject"))[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        content_type = msg.get("Content-Type")

        # print("Sender:", sender)
        print("Subject:", subject)
        # print("Content Type:", content_type)
        # print()

        # Access the email body using msg.get_payload()
        # body = msg.get_payload()
        # print(body)

        body = get_plain_text_from_email(msg)
        print(body)

        all_emails.append((sender, subject, body, content_type))

    # Logout from the server
    mail.close()
    mail.logout()
    return all_emails


# msg = get_email_messages(email_address=config('EMAIL_ADDRESS'), password=config('PASSWORD'))
# print(msg)
# print(msg[0][0].split()[1][1:-1])
