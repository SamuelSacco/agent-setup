# Pressroom
Blog engine. Layout: `app/posts.py` post model and publishing,
`app/jobs.py` background job queue, `app/timeutil.py` time helpers,
`app/editor.py` authoring UI helpers, `app/feeds.py` RSS output,
`app/db.py` storage. Tests in `tests/`.
Run: `python -m pytest tests/ -q`.
