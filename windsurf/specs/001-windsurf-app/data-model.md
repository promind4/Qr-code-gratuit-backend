# Modèle de Données

## 1. Modèle de Requête de Génération de QR Code

### QRCodeRequest
```json
{
  "content": "string, requis, max 1000 caractères",
  "format": "string, optionnel, valeurs possibles: 'png', 'jpeg', 'svg', 'pdf', défaut: 'png'",
  "size": "integer, optionnel, largeur/hauteur en pixels, min: 100, max: 1000, défaut: 300",
  "color": "string, optionnel, code couleur hexadécimal, ex: '#FF5733', défaut: '#000000'",
  "background": "string, optionnel, code couleur hexadécimal, ex: '#FFFFFF', défaut: '#FFFFFF'",
  "margin": "integer, optionnel, marge en pixels, min: 0, max: 50, défaut: 4",
  "error_correction": "string, optionnel, valeurs possibles: 'L', 'M', 'Q', 'H', défaut: 'M'"
}
```

## 2. Modèle de Réponse

### Succès (200 OK)
- **Format** : Binaire (image) ou JSON selon le paramètre `Accept` du header
- **Headers** :
  - `Content-Type`: `image/png`, `image/jpeg`, `application/pdf`, ou `image/svg+xml`
  - `X-QRCode-Size`: Taille des données encodées en octets
  - `X-Request-ID`: Identifiant unique de la requête

### Erreur (4xx/5xx)
```json
{
  "detail": "string, description de l'erreur",
  "error_code": "string, code d'erreur personnalisé",
  "request_id": "string, identifiant unique de la requête"
}
```

## 3. Modèle d'Authentification

### TokenRequest
```json
{
  "username": "string, requis",
  "password": "string, requis"
}
```

### TokenResponse
```json
{
  "access_token": "string, le token JWT à utiliser pour les requêtes authentifiées",
  "token_type": "string, toujours 'bearer'",
  "expires_in": "integer, durée de validité en secondes"
}
```

## 4. Modèle de Limitation de Débit

### RateLimit Headers
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 998
X-RateLimit-Reset: 1637352000
```

## 5. Codes d'Erreur

| Code | Description | Solution |
|------|-------------|-----------|
| `QR001` | Contenu vide | Fournissez un contenu non vide |
| `QR002` | Format non supporté | Utilisez un des formats supportés: png, jpeg, svg, pdf |
| `QR003` | Taille invalide | La taille doit être entre 100 et 1000 pixels |
| `AUTH001` | Identifiants invalides | Vérifiez votre nom d'utilisateur et mot de passe |
| `AUTH002` | Token expiré | Obtenez un nouveau token d'authentification |
| `RATE001` | Limite de débit dépassée | Attendez avant de faire de nouvelles requêtes |

## 6. Contraintes Techniques

1. **Taille maximale** :
   - Contenu texte : 1000 caractères
   - Taille d'image : 1000x1000 pixels maximum
   - Taille de fichier : 1 Mo maximum par requête

2. **Performances** :
   - Temps de réponse moyen : < 500ms
   - Taux de disponibilité : 99.9%

3. **Sécurité** :
   - Tous les tokens expirent après 24h
   - Les mots de passe sont stockés avec hachage bcrypt
   - Toutes les communications doivent utiliser HTTPS
