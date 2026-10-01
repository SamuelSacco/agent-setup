_sent: list[dict] = []

def send_email(to: str, subject: str, body: str) -> None:
    _sent.append({"to": to, "subject": subject, "body": body})
