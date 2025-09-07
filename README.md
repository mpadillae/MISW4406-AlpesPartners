# MISW4406 - AlpesPartners

Repositorio del proyecto del curso de **diseño y construcción de aplicaciones no monolíticas**. Este proyecto implementa un sistema distribuido usando patrones CQRS, eventos de dominio para la comunicación asíncrona entre componentes.

## 👥 Integrantes del equipo

| Nombre | Correo |
|--------|------------------|
| Miguel Fernando Padilla Espino | m.padillae@uniandes.edu.co |
| Johann Sebastian Páez Campos | js.paezc1@uniandes.edu.co |
| Julián Oliveros Forero | je.oliverosf@uniandes.edu.co |

## 📋 Tabla de contenidos
- [🏗️ Arquitectura](#%EF%B8%8F-arquitectura)
- [📁 Estructura del proyecto](#-estructura-del-proyecto)
- [🐳 Docker Compose](#-docker-compose)

## 🏗️ Arquitectura
La arquitectura del sistema está compuesta por dos servicios (alpespartners y notificaciones). AlpesPartners tiene dos módulos que se comunican de forma asíncrona a través de un broker de mensajes (Apache Pulsar):

![](https://github.com/user-attachments/assets/8b14d2d1-b6d5-4360-b03d-99495a318c7b)

El proyecto implementa una arquitectura de microservicios que utiliza:
- **Patrón CQRS**: Separación de operaciones de lectura y escritura
- **Eventos de dominio**: Para comunicación interna entre módulos del mismo contexto acotado
- **Message broker**: Apache Pulsar para el manejo de eventos
- **Docker**: Para la contenerización y orquestación de servicios

## 📁 Estructura del proyecto

```
📦 MISW4406-AlpesPartners
├─ docker-compose.yml
├─ pyproject.toml
├─ README.md
└─ src/
   ├─ alpespartners/           # Servicio principal de AlpesPartners
   │  ├─ api/                  # APIs REST
   │  ├─ config/               # Configuración de base de datos y UoW
   │  ├─ modulos/              # Módulos de dominio
   │  │  ├─ afiliaciones/      # Gestión de afiliaciones
   │  │  └─ marca/             # Gestión de marcas
   │  └─ seedwork/             # Componentes base compartidos
   └─ notificaciones/          # Servicio de mensajería y notificaciones
      ├─ main.py
      └─ requirements.txt
```

### Flujo de dependencias

1. **Aplicación** depende de **Dominio** (reglas de negocio)
2. **Infraestructura** implementa interfaces del **Dominio**
3. **Aplicación** puede interactuar directamente con **Infraestructura** para operaciones específicas
4. **Seedwork** proporciona componentes base reutilizables para todos los módulos


### Componentes principales

| Componente | Descripción |
|------------|-------------|
| **alpespartners/api** | APIs REST con endpoints para CQRS (`/afiliaciones/campana` y `/afiliaciones/campana/<id>`) |
| **alpespartners/modulos** | Módulos de dominio con separación de comandos, queries y handlers |
| **notificaciones** | Servicio que consume eventos de integración del broker |
| **seedwork** | Componentes base: entidades, eventos, comandos, queries, UoW |
| **notificaciones** | Servicio de mensajería que recibe eventos de integración |

## 🐳 Docker Compose

Para desplegar toda la arquitectura en un solo comando, utilizamos `docker-compose`.

### Prerrequisitos

Para ejecutar este proyecto necesitará:
- [Docker](https://docs.docker.com/get-docker/) y [docker compose](https://docs.docker.com/compose/install/)

### Configuración inicial

Antes de ejecutar por primera vez, siga estos pasos:

1. **Crear directorio de datos de Pulsar:**
   ```bash
   rm -r -f data/pulsar
   mkdir -p data/pulsar && chmod -R 777 data/pulsar
   ```

2. **Verificar puertos libres:**
   ```bash
   # Verificar que el puerto 5001 esté libre (cambiar en docker-compose.yml si está ocupado)
   lsof -i :5001

   # Verificar que los puertos de Pulsar estén libres
   lsof -i :6650  # Pulsar broker
   lsof -i :8080  # Pulsar admin
   ```

### Ejecutar servicios

**Iniciar todos los servicios:**
```bash
docker-compose up
```

Esto iniciará:
- **Pulsar**: Message broker (puertos 6650 y 8080)
- **AlpesPartners API**: API REST (puerto 5001)
- **Notificaciones**: Servicio que consume eventos de afiliaciones.

**Otros comandos útiles:**

```bash
# Detener el ambiente
docker-compose down

# Ejecutar en background
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Logs de un servicio específico
docker-compose logs -f alpespartners
docker-compose logs -f notificaciones
docker-compose logs -f pulsar

# Reconstruir imágenes
docker-compose up --build
```

### Probar la aplicación
Puede probar la aplicación utilizando las colecciones de Postman que se encuentran ubicadas en la carpeta `collections` en la raíz del proyecto.

### Verificar logs del servicio de notificaciones
```bash
docker-compose logs notificaciones
```

## 📄 Licencia

Copyright © 2025 - MISW4406: Diseño y construcción de aplicaciones no monolíticas.  
Universidad de los Andes - Maestría en Ingeniería de Software