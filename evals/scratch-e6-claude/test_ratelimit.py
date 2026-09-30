import time
import threading
import pytest
from ratelimit import TokenBucket


class TestTokenBucketBurst:
    """Test burst capacity: can consume up to capacity immediately."""

    def test_burst_up_to_capacity_allowed(self):
        """Verify bucket allows consuming up to capacity tokens in a burst."""
        bucket = TokenBucket(capacity=10, refill_rate=1.0)

        # Should be able to consume all 10 tokens immediately
        assert bucket.allow(10) is True

        # Next request for 1 token should fail (bucket empty)
        assert bucket.allow(1) is False

    def test_partial_burst_allowed(self):
        """Verify partial burst consumption works."""
        bucket = TokenBucket(capacity=10, refill_rate=1.0)

        # Consume 3 tokens
        assert bucket.allow(3) is True

        # Consume 4 more tokens (7 total, still under capacity)
        assert bucket.allow(4) is True

        # Consume 3 more (exactly capacity)
        assert bucket.allow(3) is True

        # Next request should fail
        assert bucket.allow(1) is False


class TestTokenBucketEmpty:
    """Test empty bucket: denies requests."""

    def test_empty_bucket_denies(self):
        """Verify empty bucket denies token requests."""
        bucket = TokenBucket(capacity=5, refill_rate=1.0)

        # Empty the bucket
        assert bucket.allow(5) is True

        # Try to take from empty bucket
        assert bucket.allow(1) is False
        assert bucket.allow(5) is False

    def test_request_exceeding_capacity_denied(self):
        """Verify requests exceeding capacity are denied."""
        bucket = TokenBucket(capacity=10, refill_rate=1.0)

        # Request more than capacity
        assert bucket.allow(11) is False

        # Bucket should still be full
        assert bucket.allow(10) is True


class TestTokenBucketRefill:
    """Test refill: tokens added over time allow requests again."""

    def test_refill_after_time_passes(self):
        """Verify bucket refills after time passes."""
        bucket = TokenBucket(capacity=5, refill_rate=2.0)  # 2 tokens/sec

        # Empty the bucket
        assert bucket.allow(5) is True
        assert bucket.allow(1) is False

        # Wait for 1 second (should get 2 tokens)
        time.sleep(1.0)

        # Should be able to consume 2 tokens
        assert bucket.allow(2) is True

        # But not 1 more (total 3 would exceed 5 refilled)
        assert bucket.allow(1) is False

    def test_refill_partial_and_continue(self):
        """Verify partial refill and continuation."""
        bucket = TokenBucket(capacity=10, refill_rate=1.0)  # 1 token/sec

        # Consume 8 tokens
        assert bucket.allow(8) is True
        assert bucket.allow(2) is True

        # Bucket empty, wait 0.5 seconds (0.5 tokens)
        time.sleep(0.5)
        assert bucket.allow(1) is False  # Still not enough

        # Wait another 0.6 seconds (1.1 more tokens, total 1.6)
        time.sleep(0.6)
        assert bucket.allow(1) is True  # Should have 1.1 tokens

    def test_refill_caps_at_capacity(self):
        """Verify refill never exceeds capacity."""
        bucket = TokenBucket(capacity=5, refill_rate=2.0)

        # Empty it partially
        assert bucket.allow(3) is True  # 2 left

        # Wait long enough to exceed capacity
        time.sleep(5.0)  # Should add 10 tokens, but cap at 5

        # Should only have 5 (not 7)
        assert bucket.allow(5) is True
        assert bucket.allow(1) is False


class TestTokenBucketEdgeCases:
    """Test edge cases and validation."""

    def test_zero_refill_rate(self):
        """Verify bucket with 0 refill rate never refills."""
        bucket = TokenBucket(capacity=1, refill_rate=0.0)

        assert bucket.allow(1) is True
        assert bucket.allow(1) is False

        # Wait and verify no refill
        time.sleep(1.0)
        assert bucket.allow(1) is False

    def test_invalid_capacity_raises(self):
        """Verify invalid capacity raises ValueError."""
        with pytest.raises(ValueError, match="capacity must be > 0"):
            TokenBucket(capacity=0, refill_rate=1.0)

        with pytest.raises(ValueError, match="capacity must be > 0"):
            TokenBucket(capacity=-1, refill_rate=1.0)

    def test_invalid_refill_rate_raises(self):
        """Verify invalid refill_rate raises ValueError."""
        with pytest.raises(ValueError, match="refill_rate must be >= 0"):
            TokenBucket(capacity=10, refill_rate=-0.1)

    def test_invalid_tokens_in_allow_raises(self):
        """Verify invalid tokens parameter raises ValueError."""
        bucket = TokenBucket(capacity=10, refill_rate=1.0)

        with pytest.raises(ValueError, match="tokens must be > 0"):
            bucket.allow(0)

        with pytest.raises(ValueError, match="tokens must be > 0"):
            bucket.allow(-1)


class TestTokenBucketThreadSafety:
    """Test thread safety: concurrent calls don't corrupt state."""

    def test_concurrent_allow_calls(self):
        """Verify concurrent allow() calls are thread-safe."""
        bucket = TokenBucket(capacity=100, refill_rate=10.0)
        results = []

        def consume_tokens():
            for _ in range(10):
                results.append(bucket.allow(1))

        threads = [threading.Thread(target=consume_tokens) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # 50 requests total, bucket starts with 100, should all succeed
        assert sum(results) == 50
        assert len(results) == 50

    def test_concurrent_empty_bucket(self):
        """Verify concurrent access to empty bucket is safe."""
        bucket = TokenBucket(capacity=10, refill_rate=1.0)
        bucket.allow(10)  # Empty it

        results = []

        def try_consume():
            for _ in range(5):
                results.append(bucket.allow(1))

        threads = [threading.Thread(target=try_consume) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All should fail (bucket empty, refill_rate too low for 15 requests)
        assert sum(results) == 0
        assert len(results) == 15
