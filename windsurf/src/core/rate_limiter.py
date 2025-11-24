from slowapi import Limiter
from slowapi.util import get_remote_address

# Configuration minimale du rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000/minute"],
)
