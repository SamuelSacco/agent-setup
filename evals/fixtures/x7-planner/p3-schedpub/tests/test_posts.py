from datetime import datetime, timezone
from app.posts import create_post, publish, list_published

def test_publish_transition():
    post = create_post("hello", "Hello", "body")
    publish(post, datetime.now(timezone.utc))
    assert post.status == "published"
    assert list_published() == [post]
