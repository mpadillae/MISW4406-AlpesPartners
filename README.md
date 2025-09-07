# Tutorial 5 - CQRS y manejo de eventos

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&repo=MISW4406/tutorial-5-cqrs-eventos)

Repositorio con código base para el uso de un sistema usando el patrón CQRS y usando eventos de dominio e integración para la comunicación asíncrona entre componentes internos parte del mismo contexto acotado y sistemas externos.

Este repositorio está basado en el repositorio de sidecars visto en el tutorial 4 del curso. Por tal motivo, puede usar ese mismo repositorio para entender algunos detalles que este README no cubre.

## Arquitectura

La arquitectura del sistema está compuesta por dos servicios principales que se comunican de forma asíncrona a través de un broker de mensajes (Pulsar):

<img width="3228" height="387" alt="Arquitectura del Sistema" src="https://github.com/user-attachments/assets/673a55e4-4d0b-47f7-baad-42a85d89b64d" />

### Componentes de la Arquitectura

**AlpesPartners (Servicio Principal):**

- Implementa una arquitectura hexagonal con tres capas principales
- Contiene dos módulos de negocio: **Afiliaciones** y **Marca**
- Cada módulo sigue el patrón de dependencias: Aplicación → Dominio ← Infraestructura
- Incluye componentes de soporte: **API**, **Config** y **Seedwork**

**Notificaciones (Servicio de Mensajería):**

- Servicio independiente que consume eventos de integración
- Se comunica con AlpesPartners a través del broker de mensajes
- Procesa eventos de campañas creadas y envía notificaciones

### Flujo de Dependencias

1. **Aplicación** depende de **Dominio** (reglas de negocio)
2. **Infraestructura** implementa interfaces del **Dominio**
3. **Aplicación** puede interactuar directamente con **Infraestructura** para operaciones específicas
4. **Seedwork** proporciona componentes base reutilizables para todos los módulos

## Estructura del proyecto

Este repositorio implementa una arquitectura de microservicios con patrones CQRS y manejo de eventos, organizada en dos servicios principales:

### Servicios Principales

#### 1. **AlpesPartners** (Servicio Principal)

Sistema principal que maneja la lógica de negocio de afiliaciones y marca, implementando una arquitectura hexagonal con separación clara de capas:

**Estructura de Módulos:**

- **afiliaciones/**: Módulo de gestión de afiliaciones e influencers
  - `aplicacion/`: Capa de aplicación con comandos, queries y handlers
  - `dominio/`: Capa de dominio con entidades, eventos y reglas de negocio
  - `infraestructura/`: Capa de infraestructura con repositorios, DTOs y consumidores
- **marca/**: Módulo de gestión de marca y usuarios
  - `aplicacion/`: Capa de aplicación con comandos, queries y handlers
  - `dominio/`: Capa de dominio con entidades y objetos de valor
  - `infraestructura/`: Capa de infraestructura con DTOs y consumidores

**Componentes de Soporte:**

- **api/**: API REST con endpoints para afiliaciones y marca
- **config/**: Configuración de base de datos y unidad de trabajo
- **seedwork/**: Componentes base reutilizables
  - `aplicacion/`: Comandos, queries y handlers base
  - `dominio/`: Entidades, eventos y servicios base
  - `infraestructura/`: UoW, esquemas y utilidades
  - `presentacion/`: API base

#### 2. **Notificaciones** (Servicio de Mensajería)

Servicio independiente que consume eventos de integración del broker de mensajes:

- `main.py`: Punto de entrada que consume eventos de campañas creadas

### Arquitectura por Capas

Cada módulo de negocio (afiliaciones, marca) sigue una arquitectura hexagonal:

1. **Capa de Aplicación** (`aplicacion/`):

   - `comandos/`: Comandos CQRS para operaciones de escritura
   - `queries/`: Queries CQRS para operaciones de lectura
   - `handlers.py`: Manejadores de comandos, queries y eventos
   - `servicios.py`: Servicios de aplicación

2. **Capa de Dominio** (`dominio/`):

   - `entidades.py`: Entidades de negocio
   - `eventos.py`: Eventos de dominio
   - `objetos_valor.py`: Objetos de valor
   - `servicios.py`: Servicios de dominio
   - `reglas.py`: Reglas de negocio

3. **Capa de Infraestructura** (`infraestructura/`):
   - `repositorios.py`: Implementación de repositorios
   - `consumidores.py`: Consumidores de eventos del broker
   - `despachadores.py`: Despachadores de eventos
   - `dto.py`: Objetos de transferencia de datos
   - `schema/`: Esquemas de eventos de integración (v1/)

### Patrones Implementados

- **CQRS**: Separación de comandos (escritura) y queries (lectura)
- **Event Sourcing**: Eventos de dominio para cambios de estado
- **Hexagonal Architecture**: Separación clara entre dominio, aplicación e infraestructura
- **Event-Driven Architecture**: Comunicación asíncrona entre servicios via broker de mensajes

## AlpesPartners

### Ejecutar pruebas

```bash
coverage run -m pytest
```

### Ver reporte de covertura

```bash
coverage report
```

## Docker-compose

Para desplegar toda la arquitectura en un solo comando, usamos `docker-compose`.

### Prerequisitos

Antes de ejecutar por primera vez, siga estos pasos:

1. **Crear directorio de datos de Pulsar:**

```bash
mkdir -p data/pulsar && chmod -R 777 data/pulsar
```

2. **Verificar puertos libres:**

```bash
# Verificar que el puerto 5001 esté libre (si está ocupado, cambiar por otro puerto en docker-compose.yml)
lsof -i :5001

# Verificar que los puertos de Pulsar estén libres
lsof -i :6650
lsof -i :8080
```

### Ejecutar todos los servicios

Desde el directorio principal, ejecute el siguiente comando para desplegar Pulsar + AlpesPartners API + Servicio de Notificaciones:

```bash
docker-compose up
```

Esto iniciará:

- **Pulsar**: Message broker (puertos 6650 y 8080)
- **AlpesPartners API**: API REST en http://localhost:5001
- **Notificaciones**: Servicio que consume eventos de reservas

### Otros comandos útiles

Si desea detener el ambiente ejecute:

```bash
docker-compose down
```

En caso de querer desplegar en background:

```bash
docker-compose up -d
```

Para ver logs en tiempo real:

```bash
# Todos los servicios
docker-compose logs -f

# Solo un servicio específico
docker-compose logs -f alpespartners
docker-compose logs -f notificaciones
docker-compose logs -f pulsar
```

Para reconstruir las imágenes:

```bash
docker-compose up --build
```

### Probar la aplicación

Una vez que todos los servicios estén ejecutándose, puede probar el flujo completo de eventos:

```bash
# 1. Crear una reserva (esto debería disparar un evento)
curl -X POST http://localhost:5001/vuelos/reserva \
  -H "Content-Type: application/json" \
  -d '{
    "fecha_creacion": "2025-09-03T12:00:00Z",
    "fecha_actualizacion": "2025-09-03T12:00:00Z",
    "id": "test-reserva-123",
    "itinerarios": [
        {
            "odos": [
                {
                    "segmentos": [
                        {
                            "legs": [
                                {
                                    "fecha_salida": "2022-11-22T13:10:00Z",
                                    "fecha_llegada": "2022-11-22T15:10:00Z",
                                    "destino": {
                                        "codigo": "sasads",
                                        "nombre": "John F. Kennedy International Airport"
                                    },
                                    "origen": {
                                        "codigo": "gggg",
                                        "nombre": "El Dorado - Bogotá International Airport (BOG)"
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
  }'

# 2. Verificar logs del servicio de notificaciones para ver el evento procesado
docker-compose logs notificaciones
```

Si todo funciona correctamente, deberías ver en los logs de notificaciones algo como:

```
=========================================
Mensaje Recibido: 'id_reserva=test-reserva-123, id_cliente=...'
=========================================
==== Envía correo a usuario ====
```
