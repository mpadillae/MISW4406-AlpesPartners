#!/usr/bin/env python3
"""
Script para generar datos de prueba para los microservicios de campañas
"""

import json
import uuid
import random
from datetime import datetime, timedelta


def generate_campaign_data():
    """Genera datos de campaña de prueba"""
    campaign_types = ["influencer", "afiliado", "mixta"]
    campaign_names = [
        "Campaña de Verano 2024",
        "Black Friday 2024",
        "Campaña de Primavera",
        "Cyber Monday",
        "Campaña de Navidad",
        "Día de la Madre",
        "Campaña de Back to School",
        "Valentine's Day Special"
    ]

    descriptions = [
        "Promoción especial de productos de temporada",
        "Campaña de marketing digital con influencers",
        "Programa de afiliados para el trimestre",
        "Campaña mixta de influencers y afiliados",
        "Promoción de lanzamiento de producto",
        "Campaña de retención de clientes",
        "Marketing estacional con múltiples canales"
    ]

    return {
        "id_marca": str(uuid.uuid4()),
        "nombre": random.choice(campaign_names),
        "descripcion": random.choice(descriptions),
        "tipo": random.choice(campaign_types),
        "presupuesto": round(random.uniform(5000, 100000), 2)
    }


def generate_tracking_event_data(campaign_id):
    """Genera datos de evento de tracking"""
    event_types = ["vista", "clic", "conversion",
                   "engagement", "compartir", "comentario"]
    platforms = ["instagram", "facebook", "twitter", "tiktok", "youtube"]
    devices = ["mobile", "desktop", "tablet"]

    event_type = random.choice(event_types)
    base_data = {
        "id_campana": campaign_id,
        "tipo_evento": event_type,
        "datos": {
            "usuario": f"user_{random.randint(1000, 9999)}",
            "timestamp": int(datetime.now().timestamp()),
            "plataforma": random.choice(platforms),
            "dispositivo": random.choice(devices)
        }
    }

    # Agregar datos específicos según el tipo de evento
    if event_type == "vista":
        base_data["datos"]["duracion_vista"] = random.randint(1, 300)
        base_data["datos"]["fuente"] = random.choice(
            ["feed", "story", "reel", "post"])

    elif event_type == "clic":
        base_data["datos"]["elemento"] = random.choice(
            ["boton_cta", "enlace", "imagen", "video"])
        base_data["datos"]["posicion"] = random.choice(
            ["header", "footer", "sidebar", "content"])

    elif event_type == "conversion":
        base_data["datos"]["valor_compra"] = round(random.uniform(10, 1000), 2)
        base_data["datos"]["producto"] = f"producto_{random.randint(1, 100):03d}"
        base_data["datos"]["categoria"] = random.choice(
            ["moda", "tecnologia", "belleza", "hogar"])

    elif event_type == "engagement":
        base_data["datos"]["valor"] = round(random.uniform(0.1, 1.0), 2)
        base_data["datos"]["tipo"] = random.choice(
            ["like", "comentario", "guardar", "compartir"])
        base_data["datos"]["sentimiento"] = random.choice(
            ["positivo", "neutral", "negativo"])

    elif event_type == "compartir":
        base_data["datos"]["tipo_contenido"] = random.choice(
            ["post", "story", "reel", "video"])
        base_data["datos"]["audiencia"] = random.choice(
            ["publico", "amigos", "seguidores"])

    elif event_type == "comentario":
        base_data["datos"]["texto"] = random.choice([
            "¡Me encanta este producto!",
            "Muy buena calidad",
            "Lo recomiendo totalmente",
            "Excelente servicio",
            "Perfecto para mi",
            "Muy satisfecho con la compra"
        ])
        base_data["datos"]["sentimiento"] = random.choice(
            ["positivo", "neutral"])

    return base_data


def generate_batch_events(campaign_id, count=10):
    """Genera múltiples eventos para una campaña"""
    events = []
    for _ in range(count):
        events.append(generate_tracking_event_data(campaign_id))
    return events


def main():
    """Función principal para generar datos de prueba"""
    print("🎯 Generando datos de prueba para microservicios de campañas...")

    # Generar datos de campaña
    campaigns = []
    for i in range(5):
        campaign = generate_campaign_data()
        campaigns.append(campaign)
        print(f"📋 Campaña {i+1}: {campaign['nombre']} ({campaign['tipo']})")

    # Generar eventos de tracking para cada campaña
    all_events = []
    for i, campaign in enumerate(campaigns):
        campaign_id = str(uuid.uuid4())  # Simular ID de campaña creada
        events = generate_batch_events(campaign_id, random.randint(5, 15))
        all_events.extend(events)
        print(f"📊 Generados {len(events)} eventos para campaña {i+1}")

    # Guardar datos en archivos JSON
    with open('test_campaigns.json', 'w', encoding='utf-8') as f:
        json.dump(campaigns, f, indent=2, ensure_ascii=False)

    with open('test_events.json', 'w', encoding='utf-8') as f:
        json.dump(all_events, f, indent=2, ensure_ascii=False)

    # Generar script de curl para pruebas
    curl_script = generate_curl_script(campaigns, all_events)
    with open('test_curl_script.sh', 'w', encoding='utf-8') as f:
        f.write(curl_script)

    print(f"\n✅ Datos generados exitosamente:")
    print(f"   📋 {len(campaigns)} campañas en test_campaigns.json")
    print(f"   📊 {len(all_events)} eventos en test_events.json")
    print(f"   🐚 Script de curl en test_curl_script.sh")
    print(f"\n🚀 Para usar los datos:")
    print(f"   1. Importa test_campaigns.json y test_events.json en Postman")
    print(f"   2. O ejecuta: chmod +x test_curl_script.sh && ./test_curl_script.sh")


def generate_curl_script(campaigns, events):
    """Genera un script de curl para probar las APIs"""
    script = "#!/bin/bash\n\n"
    script += "echo '🧪 Ejecutando pruebas con curl...'\n\n"

    # Variables
    script += "BASE_URL_AFILIACIONES='http://localhost:8001'\n"
    script += "BASE_URL_TRACKING='http://localhost:8004'\n\n"

    # Función helper
    script += "make_request() {\n"
    script += "    local method=$1\n"
    script += "    local url=$2\n"
    script += "    local data=$3\n"
    script += "    \n"
    script += "    if [ -n \"$data\" ]; then\n"
    script += "        curl -s -X \"$method\" \"$url\" \\\n"
    script += "            -H \"Content-Type: application/json\" \\\n"
    script += "            -d \"$data\"\n"
    script += "    else\n"
    script += "        curl -s -X \"$method\" \"$url\"\n"
    script += "    fi\n"
    script += "}\n\n"

    # Health checks
    script += "echo '🏥 Verificando servicios...'\n"
    script += "make_request GET \"$BASE_URL_AFILIACIONES/health\"\n"
    script += "make_request GET \"$BASE_URL_TRACKING/health\"\n\n"

    # Crear campañas
    script += "echo '📋 Creando campañas...'\n"
    for i, campaign in enumerate(campaigns):
        campaign_json = json.dumps(campaign, ensure_ascii=False)
        script += f"echo 'Creando campaña {i+1}...'\n"
        script += f"make_request POST \"$BASE_URL_AFILIACIONES/afiliaciones/campana\" '{campaign_json}'\n"
        script += "echo ''\n"

    # Eventos de tracking (primeros 10)
    script += "echo '📊 Registrando eventos de tracking...'\n"
    for i, event in enumerate(events[:10]):
        event_json = json.dumps(event, ensure_ascii=False)
        script += f"echo 'Registrando evento {i+1}...'\n"
        script += f"make_request POST \"$BASE_URL_TRACKING/tracking/evento\" '{event_json}'\n"
        script += "echo ''\n"

    script += "echo '✅ Pruebas completadas!'\n"

    return script


if __name__ == "__main__":
    main()
