param(
    [switch]$UseDocker, 
    [switch]$Rebuild
)

$envFile = Join-Path (Get-Location) ".env"
if (-Not (Test-Path $envFile)) {
    Copy-Item .env.example .env -Force
    Write-Host "Fichier .env généré à partir de .env.example"
}

if ($UseDocker.IsPresent) {
    $command = "docker-compose up --build"
    if (-Not $Rebuild) {
        $command = "docker-compose up"
    }
    Write-Host "Lancement de Docker Compose... ($command)" -ForegroundColor Cyan
    iex $command
    return
}

Write-Host "Préparation d'un environnement local..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
Write-Host "Démarrage de l'application FastAPI en mode développement..." -ForegroundColor Green
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
