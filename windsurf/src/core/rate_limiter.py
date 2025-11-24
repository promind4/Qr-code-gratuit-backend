import os
from slowapi import Limiter
from slowapi.util import get_remote_address

# --- FIX POUR RENDER ---
# SlowAPI cherche obligatoirement un fichier .env.
# S'il n'existe pas (cas du déploiement), on le crée vide à la volée.
if not os.path.exists(".env"):
    with open(".env", "w") as f:
        pass 
# -----------------------

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000/minute"],
    enabled=True
)












