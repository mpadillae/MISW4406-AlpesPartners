#!/bin/bash

echo "🚀 Iniciando microservicios de campañas..."

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

# Verificar que Docker Compose esté instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi

# Crear red para los microservicios
echo "📡 Creando red para microservicios..."
docker network create microservices-network 2>/dev/null || true

# Levantar servicios
echo "🐳 Levantando servicios con Docker Compose..."
docker-compose up -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 30

# Verificar estado de los servicios
echo "🔍 Verificando estado de los servicios..."

services=("afiliaciones-service:8001" "marca-service:8002" "influencer-service:8003" "tracking-service:8004")

for service in "${services[@]}"; do
    IFS=':' read -r name port <<< "$service"
    if curl -s "http://localhost:$port/health" > /dev/null; then
        echo "✅ $name está funcionando correctamente"
    else
        echo "❌ $name no está respondiendo"
    fi
done

echo ""
echo "🎉 ¡Microservicios iniciados correctamente!"
echo ""
echo "📋 Servicios disponibles:"
echo "  • Afiliaciones: http://localhost:8001"
echo "  • Marca: http://localhost:8002"
echo "  • Influencer: http://localhost:8003"
echo "  • Tracking: http://localhost:8004"
echo "  • Pulsar Admin: http://localhost:8080"
echo ""
echo "🗄️ Bases de datos:"
echo "  • Afiliaciones: localhost:5436"
echo "  • Marca: localhost:5433"
echo "  • Influencer: localhost:5434"
echo "  • Tracking: localhost:5435"
echo ""
echo "📚 Documentación API:"
echo "  • Afiliaciones: http://localhost:8001/docs"
echo "  • Marca: http://localhost:8002/docs"
echo "  • Influencer: http://localhost:8003/docs"
echo "  • Tracking: http://localhost:8004/docs"
echo ""
echo "🛑 Para detener los servicios: docker-compose down"
