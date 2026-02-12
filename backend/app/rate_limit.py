import time
from collections import defaultdict
from fastapi import Request, Depends

from app.exceptions import RateLimitError

# In-memory store: {ip: [(timestamp, ...), ...]}
_request_log: dict[str, list[float]] = defaultdict(list)

# Auth endpoints: 10 requests per 60 seconds per IP
AUTH_RATE_LIMIT = 10
AUTH_RATE_WINDOW = 60  # seconds


def _clean_old_entries(ip: str, window: int) -> None:
    cutoff = time.monotonic() - window
    _request_log[ip] = [t for t in _request_log[ip] if t > cutoff]


async def auth_rate_limit(request: Request) -> None:
    ip = request.client.host if request.client else "unknown"
    _clean_old_entries(ip, AUTH_RATE_WINDOW)

    if len(_request_log[ip]) >= AUTH_RATE_LIMIT:
        raise RateLimitError()

    _request_log[ip].append(time.monotonic())
