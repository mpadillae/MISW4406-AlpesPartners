.PHONY: help build up down logs test clean

help: ## Mostrar ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Construir todas las imágenes Docker
	docker-compose build

up: ## Levantar todos los servicios
	docker-compose up -d

down: ## Detener todos los servicios
	docker-compose down

logs: ## Ver logs de todos los servicios
	docker-compose logs -f

logs-afiliaciones: ## Ver logs del servicio de afiliaciones
	docker-compose logs -f afiliaciones-service

logs-marca: ## Ver logs del servicio de marca
	docker-compose logs -f marca-service

logs-influencer: ## Ver logs del servicio de influencer
	docker-compose logs -f influencer-service

logs-tracking: ## Ver logs del servicio de tracking
	docker-compose logs -f tracking-service

test: ## Ejecutar pruebas del flujo completo
	./test_flow.sh

start: ## Iniciar servicios con script de inicio
	./start.sh

status: ## Verificar estado de los servicios
	@echo "Verificando estado de los servicios..."
	@curl -s http://localhost:8001/health && echo " ✅ Afiliaciones" || echo " ❌ Afiliaciones"
	@curl -s http://localhost:8002/health && echo " ✅ Marca" || echo " ❌ Marca"
	@curl -s http://localhost:8003/health && echo " ✅ Influencer" || echo " ❌ Influencer"
	@curl -s http://localhost:8004/health && echo " ✅ Tracking" || echo " ❌ Tracking"

clean: ## Limpiar contenedores y volúmenes
	docker-compose down -v
	docker system prune -f

restart: down up ## Reiniciar todos los servicios

dev-afiliaciones: ## Ejecutar servicio de afiliaciones en modo desarrollo
	cd afiliaciones && uvicorn main:app --reload --port 8001

dev-marca: ## Ejecutar servicio de marca en modo desarrollo
	cd marca && uvicorn main:app --reload --port 8002

dev-influencer: ## Ejecutar servicio de influencer en modo desarrollo
	cd influencer && uvicorn main:app --reload --port 8003

dev-tracking: ## Ejecutar servicio de tracking en modo desarrollo
	cd tracking && uvicorn main:app --reload --port 8004

# Comandos de pruebas
generate-test-data: ## Generar datos de prueba para Postman
	python3 generate_test_data.py

postman-import: ## Mostrar instrucciones para importar en Postman
	@echo "📥 Para importar en Postman:"
	@echo "1. Abre Postman"
	@echo "2. Haz clic en 'Import'"
	@echo "3. Selecciona los archivos:"
	@echo "   - Microservicios_Campanas.postman_collection.json"
	@echo "   - Microservicios_Campanas.postman_environment.json"
	@echo "4. Selecciona el entorno 'Microservicios de Campañas - Local'"

test-postman: ## Ejecutar pruebas con datos generados
	./generate_test_data.py
	chmod +x test_curl_script.sh
	./test_curl_script.sh

clean-test-data: ## Limpiar archivos de datos de prueba
	rm -f test_campaigns.json test_events.json test_curl_script.sh

# Comandos de verificación
check-ports: ## Verificar puertos en uso
	@echo "🔍 Verificando puertos en uso..."
	@echo "Servicios web:"
	@lsof -i :8001 -i :8002 -i :8003 -i :8004 2>/dev/null || echo "  No hay conflictos en puertos de servicios"
	@echo "Bases de datos:"
	@lsof -i :5433 -i :5434 -i :5435 -i :5436 2>/dev/null || echo "  No hay conflictos en puertos de bases de datos"
	@echo "Pulsar:"
	@lsof -i :6650 -i :8080 2>/dev/null || echo "  No hay conflictos en puertos de Pulsar"

check-services: ## Verificar que todos los servicios estén funcionando
	@echo "🏥 Verificando servicios..."
	@curl -s http://localhost:8001/health > /dev/null && echo "✅ Afiliaciones" || echo "❌ Afiliaciones"
	@curl -s http://localhost:8002/health > /dev/null && echo "✅ Marca" || echo "❌ Marca"
	@curl -s http://localhost:8003/health > /dev/null && echo "✅ Influencer" || echo "❌ Influencer"
	@curl -s http://localhost:8004/health > /dev/null && echo "✅ Tracking" || echo "❌ Tracking"
	@curl -s http://localhost:8080/admin/v2/clusters > /dev/null && echo "✅ Pulsar" || echo "❌ Pulsar"

show-ports: ## Mostrar configuración de puertos
	@echo "🚪 Configuración de puertos:"
	@echo "Servicios web:"
	@echo "  • Afiliaciones: http://localhost:8001"
	@echo "  • Marca: http://localhost:8002"
	@echo "  • Influencer: http://localhost:8003"
	@echo "  • Tracking: http://localhost:8004"
	@echo "  • Pulsar Admin: http://localhost:8080"
	@echo "Bases de datos:"
	@echo "  • Afiliaciones: localhost:5436"
	@echo "  • Marca: localhost:5433"
	@echo "  • Influencer: localhost:5434"
	@echo "  • Tracking: localhost:5435"
