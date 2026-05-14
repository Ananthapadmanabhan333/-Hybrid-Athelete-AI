@echo off
echo Fuelix Production Deployment Script
echo -----------------------------------

docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: docker is required but not installed.
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: docker-compose is required but not installed.
    exit /b 1
)

if not exist ".env" (
    echo Warning: .env file missing in production. Using defaults or .env.example.
    echo Copying .env.example to .env for you. PLEASE CHANGE THESE CREDENTIALS.
    copy .env.example .env
)

echo Bringing down any existing containers...
docker-compose -f docker-compose.prod.yml down

echo Building full production stack...
docker-compose -f docker-compose.prod.yml build

echo Starting application...
docker-compose -f docker-compose.prod.yml up -d

echo.
echo Deployment successful.
echo Application running on:
echo Frontend: http://localhost
echo API Backend: http://localhost/api/v1 (Proxied via Nginx)
echo.
echo If running on a VPS or cloud droplet, replace localhost with your public IP/domain.
pause
