Write-Host ""
Write-Host "========================================="
Write-Host " AI Bootcamp Day 8 - Pathfinding Project"
Write-Host "========================================="
Write-Host ""

Write-Host "[1/4] Installing dependencies..."
python -m pip install -r requirements.txt

Write-Host ""
Write-Host "[2/4] Running unit tests..."
python -m pytest

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Tests failed. Exiting..."
    exit 1
}

Write-Host ""
Write-Host "[3/4] Building Docker image..."
docker compose build

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Docker build failed."
    exit 1
}

Write-Host ""
Write-Host "[4/4] Starting Flask application..."
Write-Host "Open http://localhost:60003"
Write-Host ""

python app.py