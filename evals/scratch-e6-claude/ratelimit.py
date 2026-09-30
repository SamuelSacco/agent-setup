import threading
import time


class TokenBucket:
    """Token bucket rate limiter.

    Implements the token bucket algorithm for rate limiting.
    Allows bursts up to capacity, then refills at refill_rate tokens/sec.
    Thread-safe via internal lock.
    """

    def __init__(self, capacity: int, refill_rate: float):
        """Initialize token bucket.

        Args:
            capacity: Maximum tokens in bucket (e.g., 10)
            refill_rate: Tokens added per second (e.g., 2.0)

        Raises:
            ValueError: If capacity <= 0 or refill_rate < 0
        """
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        if refill_rate < 0:
            raise ValueError("refill_rate must be >= 0")

        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)  # Start full
        self.last_refill_time = time.time()
        self._lock = threading.Lock()

    def allow(self, tokens: int = 1) -> bool:
        """Attempt to consume tokens from the bucket.

        Automatically refills based on elapsed time since last call.

        Args:
            tokens: Number of tokens to consume (default 1)

        Returns:
            True if tokens were granted and consumed, False otherwise

        Raises:
            ValueError: If tokens <= 0
        """
        if tokens <= 0:
            raise ValueError("tokens must be > 0")

        with self._lock:
            # Refill based on elapsed time
            now = time.time()
            elapsed = now - self.last_refill_time
            refilled = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + refilled)
            self.last_refill_time = now

            # Check if we can consume
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            else:
                return False
