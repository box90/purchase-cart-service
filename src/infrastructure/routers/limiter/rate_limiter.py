from slowapi import Limiter
from slowapi.util import get_remote_address

# Just a simple rateLimiter
limiter = Limiter(key_func=get_remote_address)