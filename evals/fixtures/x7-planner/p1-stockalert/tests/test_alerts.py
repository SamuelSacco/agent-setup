from app import alerts

def test_send_email_records():
    alerts.send_email("a@b.c", "s", "b")
    assert alerts._sent[-1]["subject"] == "s"
