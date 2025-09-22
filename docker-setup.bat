@echo off
REM HDBank Chatbot Docker Setup Script for Windows

echo 🏦 HDBank Chatbot - Docker Setup
echo ==================================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not available. Please install Docker Desktop with Compose.
    pause
    exit /b 1
)

REM Create necessary directories
echo 📁 Creating directories...
if not exist uploads mkdir uploads
if not exist logs mkdir logs
if not exist ssl mkdir ssl

REM Copy environment file if it doesn't exist
if not exist .env (
    echo 📋 Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please edit .env file and add your GEMINI_API_KEY
)

REM Build and start services
echo 🔨 Building Docker images...
docker-compose build

echo 🚀 Starting services...
docker-compose up -d

REM Wait for services to be ready
echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak >nul

REM Setup database
echo 🗄️ Setting up database...
docker-compose exec hdbank-chatbot python setup_database.py

REM Show status
echo 📊 Service status:
docker-compose ps

echo.
echo ✅ Setup complete!
echo 🌐 Application: http://localhost:8000
echo ⚙️ Admin Panel: http://localhost:8000/admin.html
echo 🗄️ Database: localhost:5432
echo.
echo 📋 Useful commands:
echo   docker-compose logs -f            # View logs
echo   docker-compose stop               # Stop services
echo   docker-compose down               # Stop and remove containers
echo   docker-compose exec hdbank-chatbot bash  # Access container shell

pause