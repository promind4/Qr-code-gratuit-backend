# QR Code Generation API

API stateless pour générer des QR codes à partir de texte ou d'URL avec personnalisation
(marges, couleurs, correction d'erreur) et plusieurs formats de sortie (PNG, JPEG, SVG, PDF).
Les QR codes ne sont **pas stockés** : chaque requête retourne immédiatement un binaire.

## Structure du projet
- `src/`: logique FastAPI (routers, services, middleware).
- `tests/`: tests unitaires et d'intégration.
- `specs/001-windsurf-app/`: toute la documentation de spécification (plan, données, tâches, quickstart, recherche).

## Pré-requis
- Python 3.11 ou supérieur
- Docker & docker-compose (recommandé pour lancer l'API de manière isolée)
- `pip install -r requirements.txt` pour l'exécution locale sans conteneurs

## Démarrage rapide
1. Copier le fichier d'exemple :
   ```bash
   cp .env.example .env
   # mettre à jour JWT_SECRET_KEY et autres variables si nécessaire
   ```
2. Lancer l'API via Docker Compose :
   ```bash
   docker-compose up --build
   ```
3. L'API écoute sur `http://localhost:8000` avec documentation interactive OpenAPI
   (`http://localhost:8000/docs`)

## Authentification
- Un seul utilisateur fictif existe par défaut :
  - `username`: `developer`
  - `password`: `devpass123`
- Obtenir un token :
  ```bash
  curl -X POST http://localhost:8000/api/v1/auth/token \
    -H "Content-Type: application/json" \
    -d '{"username": "developer", "password": "devpass123"}'
  ```
- Inclure le JWT dans le header `Authorization: Bearer <token>` pour les endpoints protégés.

## Génération de QR
- Exemple minimal (PNG) et options avancées décrites dans `specs/001-windsurf-app/quickstart.md`.
- L'endpoint `/api/v1/qrcode/generate` renvoie :
  - le binaire du QR code dans la bonne `Content-Type`
  - des headers `X-QRCode-Request-ID` et `X-QRCode-Size`
  - validation stricte via Pydantic (`content`, `format`, `size`, `color`, `error_correction`).

## Tests
```bash
pip install -r requirements.txt
pytest
```
Les tests couvrent :
- le service QR (PNG, JPEG, SVG, PDF, validations) : `tests/unit/test_qrcode_service.py`
- le flux d'authentification JWT (succès / échec) : `tests/integration/test_auth_flow.py`

## Déploiement
- Construire l'image Docker : `docker-compose build`
- Déployer sur un orchestrateur (Kubernetes, AWS App Runner, etc.) en réutilisant la même image.
- Configurer les secrets JWT via des variables d'environnement ou un gestionnaire sécurisé.

## Documentation et suites
Les spécifications détaillées (requirements, modèles de données, plan, tâches, quickstart, recherches) sont disponibles dans `specs/001-windsurf-app/` pour référence et planification.
