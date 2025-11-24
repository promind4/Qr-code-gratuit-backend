# Guide de démarrage rapide - API de Génération de QR Codes

## Prérequis
- Python 3.11 ou supérieur
- pip (gestionnaire de paquets Python)
- Un compte développeur pour obtenir une clé API

## Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/votre-utilisateur/qrcode-api.git
   cd qrcode-api
   ```

2. **Créer un environnement virtuel** :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: .\venv\Scripts\activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement** :
   ```bash
   cp .env.example .env
   # Éditer .env avec vos paramètres
   ```

## Utilisation de base

### 1. Obtenir un token d'accès

```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username": "votre_utilisateur", "password": "votre_mot_de_passe"}'
```

Réponse :
```json
{
  "access_token": "votre_token_jwt",
  "token_type": "bearer"
}
```

### 2. Générer un QR code simple

```bash
curl -X POST "http://localhost:8000/api/v1/qrcode/generate" \
  -H "Authorization: Bearer votre_token_jwt" \
  -H "Content-Type: application/json" \
  -d '{"content": "https://exemple.com", "format": "png"}'
```

### 3. Générer un QR code personnalisé

```bash
curl -X POST "http://localhost:8000/api/v1/qrcode/generate" \
  -H "Authorization: Bearer votre_token_jwt" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "https://exemple.com",
    "format": "png",
    "size": 300,
    "color": "#FF5733",
    "background": "#FFFFFF",
    "margin": 10,
    "error_correction": "H"
  }'
```

## Exemples de code

### Python avec requests

```python
import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
TOKEN = "votre_token_jwt"

# En-têtes d'authentification
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Générer un QR code
def generate_qr_code(content, format="png", **kwargs):
    url = f"{BASE_URL}/qrcode/generate"
    data = {"content": content, "format": format, **kwargs}
    response = requests.post(url, headers=headers, json=data)
    return response

# Exemple d'utilisation
response = generate_qr_code(
    content="https://exemple.com",
    format="png",
    size=300,
    color="#FF5733"
)

# Sauvegarder le QR code généré
if response.status_code == 200:
    with open("qrcode.png", "wb") as f:
        f.write(response.content)
```

## Gestion des erreurs

L'API retourne des codes HTTP standard :

- `200 OK` : Requête réussie
- `400 Bad Request` : Données de requête invalides
- `401 Unauthorized` : Token manquant ou invalide
- `429 Too Many Requests` : Limite de débit dépassée
- `500 Internal Server Error` : Erreur serveur

## Sécurité

- Ne partagez jamais votre token JWT
- Utilisez toujours HTTPS en production
- Limitez les permissions de votre token au strict nécessaire
- Régénérez régulièrement vos tokens

## Support

Pour toute question ou problème, veuillez ouvrir une issue sur notre [dépôt GitHub](https://github.com/votre-utilisateur/qrcode-api/issues).
