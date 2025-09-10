# Microservicios de Campañas - Arquitectura Hexagonal

Este proyecto implementa un sistema de microservicios para la gestión de campañas de marketing utilizando arquitectura hexagonal y patrones de diseño como CQRS, DDD y Event-Driven Architecture.

## Arquitectura

El sistema está compuesto por 4 microservicios independientes:

### 1. AFILIACIONES (Puerto 8001)
- **Función**: Inicia el flujo de campañas
- **Endpoint**: `POST /afiliaciones/campana`
- **Eventos que publica**: `CampanaCreada`, `CampanaIniciada`
- **Base de datos**: `afiliaciones-db` (PostgreSQL - Puerto 5436)

### 2. MARCA (Puerto 8002)
- **Función**: Procesa información de marca
- **Eventos que consume**: `CampanaCreada`, `CampanaIniciada`
- **Base de datos**: `marca-db` (PostgreSQL - Puerto 5433)

### 3. INFLUENCER (Puerto 8003)
- **Función**: Gestiona influencers
- **Eventos que consume**: `CampanaCreada`, `CampanaIniciada`
- **Base de datos**: `influencer-db` (PostgreSQL - Puerto 5434)

### 4. TRACKING (Puerto 8004)
- **Función**: Rastrea métricas y eventos
- **Endpoint**: `POST /tracking/evento`
- **Eventos que consume**: `CampanaCreada`, `CampanaIniciada`
- **Base de datos**: `tracking-db` (PostgreSQL - Puerto 5435)

## Tecnologías

- **FastAPI**: Framework web para APIs
- **PostgreSQL**: Base de datos relacional
- **Apache Pulsar**: Message broker para eventos
- **SQLAlchemy**: ORM para Python
- **Pydantic**: Validación de datos
- **Docker**: Containerización

## Patrones de Diseño Implementados

### 1. Arquitectura Hexagonal
Cada microservicio sigue la arquitectura hexagonal con:
- **Dominio**: Entidades, eventos, reglas de negocio
- **Aplicación**: Casos de uso, comandos, queries
- **Infraestructura**: Repositorios, despachadores, consumidores

### 2. CQRS (Command Query Responsibility Segregation)
- **Comandos**: Operaciones de escritura (crear, actualizar)
- **Queries**: Operaciones de lectura (obtener, listar)
- **Handlers**: Manejadores específicos para cada comando/query

### 3. Domain-Driven Design (DDD)
- **Entidades**: Objetos con identidad única
- **Objetos de Valor**: Objetos inmutables
- **Eventos de Dominio**: Eventos que ocurren en el dominio
- **Repositorios**: Interfaces para acceso a datos

### 4. Event-Driven Architecture
- **Eventos de Dominio**: Comunicación asíncrona entre servicios
- **Despachadores**: Publicación de eventos
- **Consumidores**: Procesamiento de eventos

## Estructura de Archivos

```
proyecto/
├── docker-compose.yml
├── afiliaciones/
│   ├── aplicacion/
│   │   ├── comandos/
│   │   ├── queries/
│   │   ├── dto.py
│   │   ├── handlers.py
│   │   ├── mapeadores.py
│   │   └── servicios.py
│   ├── dominio/
│   │   ├── entidades.py
│   │   ├── eventos.py
│   │   ├── excepciones.py
│   │   ├── objetos_valor.py
│   │   ├── reglas.py
│   │   ├── repositorios.py
│   │   └── servicios.py
│   ├── infraestructura/
│   │   ├── consumidores.py
│   │   ├── despachadores.py
│   │   ├── repositorios.py
│   │   └── schema/
│   │       └── v1/
│   │           ├── comandos.py
│   │           └── eventos.py
│   ├── api/
│   │   └── endpoints.py
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── marca/
├── influencer/
└── tracking/
```

## Flujo de Ejemplo

1. **Cliente** llama `POST /afiliaciones/campana`
2. **Servicio Afiliaciones** crea campaña y publica evento `CampanaCreada`
3. **Servicios Marca, Influencer y Tracking** reciben el evento
4. Cada servicio procesa el evento y guarda en su BD
5. **Cliente** puede llamar `POST /tracking/evento` para registrar métricas

## Comandos para Ejecutar

### 1. Levantar todos los servicios
```bash
cd proyecto
docker-compose up -d
```

### 2. Verificar servicios
```bash
# Health checks
curl http://localhost:8001/health  # Afiliaciones
curl http://localhost:8002/health  # Marca
curl http://localhost:8003/health  # Influencer
curl http://localhost:8004/health  # Tracking
```

### 3. Crear una campaña
```bash
curl -X POST "http://localhost:8001/afiliaciones/campana" \
  -H "Content-Type: application/json" \
  -d '{
    "id_marca": "123e4567-e89b-12d3-a456-426614174000",
    "nombre": "Campaña de Verano",
    "descripcion": "Promoción de productos de verano",
    "tipo": "influencer",
    "presupuesto": 10000.0
  }'
```

### 4. Registrar evento de tracking
```bash
curl -X POST "http://localhost:8004/tracking/evento" \
  -H "Content-Type: application/json" \
  -d '{
    "id_campana": "123e4567-e89b-12d3-a456-426614174000",
    "tipo_evento": "vista",
    "datos": {"usuario": "user123", "timestamp": 1640995200}
  }'
```

## Características Adicionales

- **Logging**: Logging estructurado en cada servicio
- **Validación**: Validación de DTOs con Pydantic
- **Manejo de Errores**: Excepciones personalizadas por dominio
- **Health Checks**: Endpoint `/health` en cada servicio
- **Documentación**: Swagger/OpenAPI automático
- **Configuración**: Variables de entorno para configuración
- **Testing**: Estructura preparada para tests unitarios

## Monitoreo

- **Pulsar Admin**: http://localhost:8080
- **Bases de Datos**:
  - Afiliaciones: localhost:5436
  - Marca: localhost:5433
  - Influencer: localhost:5434
  - Tracking: localhost:5435
- **Logs**: `docker-compose logs -f [servicio]`
- **Métricas**: Endpoints de tracking disponibles

## Desarrollo

Para desarrollo local, cada servicio puede ejecutarse independientemente:

```bash
# Servicio específico
cd afiliaciones
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

## 🧪 Pruebas con Postman

El proyecto incluye una colección completa de Postman para probar todos los microservicios:

### Archivos de Prueba
- `Microservicios_Campanas.postman_collection.json` - Colección principal
- `Microservicios_Campanas.postman_environment.json` - Variables de entorno
- `POSTMAN_TESTING.md` - Guía detallada de pruebas
- `generate_test_data.py` - Generador de datos de prueba

### Comandos de Prueba
```bash
# Generar datos de prueba
make generate-test-data

# Mostrar instrucciones de importación
make postman-import

# Ejecutar pruebas con curl
make test-postman

# Limpiar datos de prueba
make clean-test-data
```

### Pruebas con Newman (CLI)
```bash
# Instalar dependencias
npm install

# Ejecutar todas las pruebas
npm test

# Ejecutar pruebas específicas
npm run test:health
npm run test:afiliaciones
npm run test:tracking
npm run test:flow

# Generar reporte HTML
npm run test:html
```

## Próximos Pasos

1. Implementar tests unitarios
2. Agregar métricas de Prometheus
3. Implementar circuit breakers
4. Agregar autenticación/autorización
5. Implementar sagas para transacciones distribuidas
