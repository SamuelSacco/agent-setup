from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Post:
    slug: str
    title: str
    body: str
    status: str = "draft"  # draft -> published (one-way)
    published_at: datetime | None = None

_posts: dict[str, Post] = {}

def create_post(slug: str, title: str, body: str) -> Post:
    post = Post(slug, title, body)
    _posts[slug] = post
    return post

def get_post(slug: str) -> Post | None:
    return _posts.get(slug)

def publish(post: Post, now: datetime) -> Post:
    """Transition a draft to published, stamping published_at."""
    post.status = "published"
    post.published_at = now
    return post

def list_published() -> list[Post]:
    return [p for p in _posts.values() if p.status == "published"]
