#!/bin/bash

# HDBank Chatbot Docker Setup Script

echo "🏦 HDBank Chatbot - Docker Setup"
echo "=================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads logs ssl

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your GEMINI_API_KEY"
fi

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Setup database
echo "🗄️ Setting up database..."
docker-compose exec hdbank-chatbot python setup_database.py

# Show status
echo "📊 Service status:"
docker-compose ps

echo ""
echo "✅ Setup complete!"
echo "🌐 Application: http://localhost:8000"
echo "⚙️ Admin Panel: http://localhost:8000/admin.html"
echo "🗄️ Database: localhost:5432"
echo ""
echo "📋 Useful commands:"
echo "  docker-compose logs -f            # View logs"
echo "  docker-compose stop               # Stop services"
echo "  docker-compose down               # Stop and remove containers"
echo "  docker-compose exec hdbank-chatbot bash  # Access container shell"