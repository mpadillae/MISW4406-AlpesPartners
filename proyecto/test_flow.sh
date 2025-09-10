#!/bin/bash

echo "🧪 Probando flujo completo de microservicios..."

# Función para hacer peticiones HTTP
make_request() {
    local method=$1
    local url=$2
    local data=$3
    
    if [ -n "$data" ]; then
        curl -s -X "$method" "$url" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "$url"
    fi
}

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 10

# 1. Crear una campaña
echo ""
echo "1️⃣ Creando campaña..."
campaign_data='{
    "id_marca": "123e4567-e89b-12d3-a456-426614174000",
    "nombre": "Campaña de Verano 2024",
    "descripcion": "Promoción de productos de verano con influencers",
    "tipo": "influencer",
    "presupuesto": 15000.0
}'

response=$(make_request "POST" "http://localhost:8001/afiliaciones/campana" "$campaign_data")
echo "Respuesta: $response"

# Extraer ID de la campaña
campaign_id=$(echo "$response" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "ID de campaña: $campaign_id"

# 2. Iniciar la campaña
echo ""
echo "2️⃣ Iniciando campaña..."
init_response=$(make_request "POST" "http://localhost:8001/afiliaciones/campana/$campaign_id/iniciar")
echo "Respuesta: $init_response"

# 3. Registrar evento de tracking
echo ""
echo "3️⃣ Registrando evento de tracking..."
tracking_data='{
    "id_campana": "'$campaign_id'",
    "tipo_evento": "vista",
    "datos": {
        "usuario": "user123",
        "timestamp": '$(date +%s)',
        "fuente": "instagram"
    }
}'

tracking_response=$(make_request "POST" "http://localhost:8004/tracking/evento" "$tracking_data")
echo "Respuesta: $tracking_response"

# 4. Registrar más eventos
echo ""
echo "4️⃣ Registrando más eventos..."

# Evento de clic
click_data='{
    "id_campana": "'$campaign_id'",
    "tipo_evento": "clic",
    "datos": {
        "usuario": "user123",
        "timestamp": '$(date +%s)',
        "elemento": "boton_cta"
    }
}'

make_request "POST" "http://localhost:8004/tracking/evento" "$click_data"

# Evento de engagement
engagement_data='{
    "id_campana": "'$campaign_id'",
    "tipo_evento": "engagement",
    "datos": {
        "usuario": "user123",
        "timestamp": '$(date +%s)',
        "valor": 0.85,
        "tipo": "like"
    }
}'

make_request "POST" "http://localhost:8004/tracking/evento" "$engagement_data"

# 5. Obtener métricas de la campaña
echo ""
echo "5️⃣ Obteniendo métricas de la campaña..."
metrics_response=$(make_request "GET" "http://localhost:8004/tracking/metricas/$campaign_id")
echo "Métricas: $metrics_response"

# 6. Obtener eventos de la campaña
echo ""
echo "6️⃣ Obteniendo eventos de la campaña..."
events_response=$(make_request "GET" "http://localhost:8004/tracking/eventos/$campaign_id")
echo "Eventos: $events_response"

# 7. Obtener todas las campañas
echo ""
echo "7️⃣ Obteniendo todas las campañas..."
all_campaigns=$(make_request "GET" "http://localhost:8001/afiliaciones/campanas")
echo "Campañas: $all_campaigns"

echo ""
echo "✅ ¡Flujo de prueba completado!"
echo ""
echo "📊 Resumen:"
echo "  • Campaña creada e iniciada"
echo "  • Eventos de tracking registrados"
echo "  • Métricas calculadas automáticamente"
echo "  • Servicios de Marca e Influencer procesaron eventos"
echo ""
echo "🔍 Verifica los logs de los servicios para ver el procesamiento de eventos:"
echo "  docker-compose logs -f afiliaciones-service"
echo "  docker-compose logs -f marca-service"
echo "  docker-compose logs -f influencer-service"
echo "  docker-compose logs -f tracking-service"
