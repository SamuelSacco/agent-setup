from app.jobs import add_job, run_pending

def test_run_pending_executes():
    seen = []
    add_job(lambda: seen.append(1))
    run_pending()
    assert seen == [1]
