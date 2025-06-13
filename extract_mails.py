import imaplib
import email
from email.header import decode_header

def login_into_gmail(imap_user, imap_password):
    print("Login to the mail")
    conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    conn.login(imap_user, imap_password)
    return conn

def extract_specific_email():
    conn = login_into_gmail('murcorpcv@gmail.com', 'ekmw pldz tdhw zkkp')
    if not conn:
        return

    conn.select("inbox")
    print("Entered to the inbox")

    status, messages = conn.search(
        None,
        '(FROM "bang@bpomails.com" SUBJECT "Fwd: Leslie Edwards, you have a new BPO order from PCV Murcor - ORDER # 3642840")'
    )
    print("The status is : ", status)

    mail_ids = messages[0].split()

    for mail_id in mail_ids:
        status, msg_data = conn.fetch(mail_id, "(RFC822)")
        # print("The status is : ", status)
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")
                from_ = msg.get("From")
                print(f"Subject: {subject}")
                print(f"From: {from_}")

                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            # print("Body:", body)
                else:
                    body = msg.get_payload(decode=True).decode()
                    # print("Body:", body)

    conn.logout()

# extract_specific_email()
