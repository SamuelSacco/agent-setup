from app.posts import list_published

def rss_items() -> list[dict]:
    # Feed reads published posts only, via list_published().
    return [{"title": p.title, "slug": p.slug} for p in list_published()]
