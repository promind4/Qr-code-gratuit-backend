from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.extension import _AppConfig

# Crée un config vide pour éviter que SlowAPI tente de lire .env
empty_config = _AppConfig()  # pas de fichier .env chargé

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000/minute"],
    enabled=True,
    config=empty_config  # on passe la config vide ici
)




