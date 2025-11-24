from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.config import Config

empty_config = Config(environ={})

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000/minute"],
    enabled=True,
    config=empty_config
)









