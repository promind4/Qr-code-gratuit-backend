# Recherche et Décisions Techniques

## 1. Choix de la Stack Technique

### Framework Web : FastAPI
- **Pourquoi ?**
  - Performances élevées avec Starlette et Pydantic
  - Support natif de l'asynchrone
  - Génération automatique de documentations OpenAPI
  - Typage fort grâce à Python 3.11
- **Alternatives évaluées** :
  - Flask : trop limité pour les API asynchrones
  - Django REST Framework : trop lourd pour un service stateless

### Génération de QR Codes
- **Bibliothèque sélectionnée** : `qrcode`
  - Support des formats PNG, JPEG, SVG
  - Paramètres de personnalisation (couleur, correction d'erreur)
  - Active maintenance
- **Alternatives** :
  - `segno` : documentation moins complète
  - `pyqrcode` : peu maintenu

## 2. Sécurité et authentification

### Token JWT
- `python-jose` pour signer et vérifier
- Durée de vie : 24h avec rafraîchissement possible
- Les tokens sont transmis via `Authorization: Bearer`
- Stockage des secrets via variables d'environnement

### Prévention des abus
- Validation d'entrée avec Pydantic
- Rate limiting par token (limite configurable)
- Taille des données limitée à 1 Mo par requête

## 3. Performance

### Objectifs
- < 500 ms de latence p95
- 1000 requêtes/s (mise à l'échelle horizontale)
- 99,9 % de disponibilité

### Optimisations envisagées
- Pas de stockage intermédiaire (stateless)
- Compression des réponses (GZIP)
- Cache HTTP pour QR codes générés fréquemment
- Mise en place de workers pour traitement de PDF

## 4. Déploiement et observabilité

### Déploiement
- Conteneur Docker (Python 3.11-slim)
- Possibilité de déployer sur Kubernetes ou AWS App Runner
- API exposée via HTTPS/2 ou HTTP/3

### Observabilité
- Logs structurés (JSON) vers un système centralisé
- Métriques exposées (Prometheus) : latence, taux d'erreur, nombre de tokens
- Alerting sur dépassement de limites ou erreurs 5xx

## 5. Améliorations futures
- Support des QR codes dynamiques (URL mise à jour)
- Intégration d’un système de monitoring de quotas
- Interface d'administration pour gérer les tokens
- Ajout d’un endpoint de validation (ping d’un QR code sans le générer)
