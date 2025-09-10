# 🚪 Configuración de Puertos

Este documento lista todos los puertos utilizados por el sistema de microservicios.

## 🌐 Servicios Web

| Servicio | Puerto | URL | Descripción |
|----------|--------|-----|-------------|
| Afiliaciones | 8001 | http://localhost:8001 | Servicio principal de campañas |
| Marca | 8002 | http://localhost:8002 | Servicio de procesamiento de marca |
| Influencer | 8003 | http://localhost:8003 | Servicio de gestión de influencers |
| Tracking | 8004 | http://localhost:8004 | Servicio de métricas y seguimiento |

## 🗄️ Bases de Datos PostgreSQL

| Servicio | Puerto | Host | Base de Datos |
|----------|--------|------|---------------|
| Afiliaciones | 5436 | localhost:5436 | afiliaciones |
| Marca | 5433 | localhost:5433 | marca |
| Influencer | 5434 | localhost:5434 | influencer |
| Tracking | 5435 | localhost:5435 | tracking |

## 📡 Apache Pulsar

| Servicio | Puerto | URL | Descripción |
|----------|--------|-----|-------------|
| Pulsar Broker | 6650 | pulsar://localhost:6650 | Message broker |
| Pulsar Admin | 8080 | http://localhost:8080 | Interfaz de administración |

## 🔧 Conexiones Internas

Los servicios se conectan entre sí usando los nombres de contenedor de Docker:

- **Afiliaciones → Afiliaciones DB**: `afiliaciones-db:5432`
- **Marca → Marca DB**: `marca-db:5432`
- **Influencer → Influencer DB**: `influencer-db:5432`
- **Tracking → Tracking DB**: `tracking-db:5432`
- **Todos → Pulsar**: `pulsar:6650`

## 🚨 Resolución de Conflictos

Si encuentras conflictos de puertos:

1. **Puerto 5432 ocupado**: La base de datos de afiliaciones usa el puerto 5436
2. **Puerto 8001 ocupado**: Cambia el puerto en docker-compose.yml
3. **Puerto 8080 ocupado**: Pulsar Admin puede usar otro puerto

### Cambiar puertos de servicios web:

```yaml
# En docker-compose.yml
afiliaciones-service:
  ports:
    - "8005:8000"  # Cambiar 8001 por 8005
```

### Cambiar puertos de bases de datos:

```yaml
# En docker-compose.yml
afiliaciones-db:
  ports:
    - "5437:5432"  # Cambiar 5436 por 5437
```

## 🔍 Verificar Puertos en Uso

```bash
# Ver puertos en uso
netstat -tulpn | grep LISTEN

# Ver puertos específicos
lsof -i :8001
lsof -i :5436
lsof -i :8080
```

## 📋 Comandos de Verificación

```bash
# Verificar servicios web
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health

# Verificar bases de datos
psql -h localhost -p 5436 -U postgres -d afiliaciones
psql -h localhost -p 5433 -U postgres -d marca
psql -h localhost -p 5434 -U postgres -d influencer
psql -h localhost -p 5435 -U postgres -d tracking

# Verificar Pulsar
curl http://localhost:8080/admin/v2/clusters
```

## 🛠️ Desarrollo Local

Para desarrollo local sin Docker:

1. **Bases de datos**: Instalar PostgreSQL localmente
2. **Pulsar**: Instalar Apache Pulsar localmente
3. **Servicios**: Ejecutar con `uvicorn main:app --reload`

### Variables de entorno para desarrollo:

```bash
# Afiliaciones
DATABASE_URL=postgresql://postgres:postgres@localhost:5436/afiliaciones
PULSAR_URL=pulsar://localhost:6650

# Marca
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/marca
PULSAR_URL=pulsar://localhost:6650

# Influencer
DATABASE_URL=postgresql://postgres:postgres@localhost:5434/influencer
PULSAR_URL=pulsar://localhost:6650

# Tracking
DATABASE_URL=postgresql://postgres:postgres@localhost:5435/tracking
PULSAR_URL=pulsar://localhost:6650
```
