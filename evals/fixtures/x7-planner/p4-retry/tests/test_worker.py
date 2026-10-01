from app.worker import enqueue, process_queue

def test_process_queue_runs_jobs():
    seen = []
    enqueue(lambda: seen.append(1))
    process_queue()
    assert seen == [1]
