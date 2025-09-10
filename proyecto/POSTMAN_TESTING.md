# 🧪 Guía de Pruebas con Postman

Esta guía te ayudará a probar todos los microservicios usando la colección de Postman incluida.

## 📋 Archivos Incluidos

- `Microservicios_Campanas.postman_collection.json` - Colección principal con todas las peticiones
- `Microservicios_Campanas.postman_environment.json` - Variables de entorno para configuración local

## 🚀 Configuración Inicial

### 1. Importar en Postman

1. Abre Postman
2. Haz clic en "Import" en la esquina superior izquierda
3. Selecciona los archivos:
   - `Microservicios_Campanas.postman_collection.json`
   - `Microservicios_Campanas.postman_environment.json`
4. Asegúrate de que el entorno "Microservicios de Campañas - Local" esté seleccionado

### 2. Levantar los Servicios

```bash
cd proyecto
./start.sh
# o
make start
```

### 3. Verificar que los Servicios Estén Funcionando

Ejecuta la carpeta "🏥 Health Checks" para verificar que todos los servicios estén respondiendo.

## 📚 Estructura de la Colección

### 🏥 Health Checks
- Verifica el estado de todos los microservicios
- Debe ejecutarse primero para confirmar que todo está funcionando

### 📋 Afiliaciones Service
- **Crear Campaña**: Crea campañas de diferentes tipos (influencer, afiliado, mixta)
- **Iniciar Campaña**: Inicia una campaña existente
- **Obtener Campaña por ID**: Consulta una campaña específica
- **Obtener Todas las Campañas**: Lista todas las campañas

### 🏷️ Marca Service
- **Health Check**: Verifica el estado del servicio
- *Nota: Este servicio solo consume eventos, no tiene endpoints REST*

### 👥 Influencer Service
- **Health Check**: Verifica el estado del servicio
- *Nota: Este servicio solo consume eventos, no tiene endpoints REST*

### 📊 Tracking Service
- **Registrar Evento**: Diferentes tipos de eventos (vista, clic, conversión, engagement, compartir, comentario)
- **Obtener Métricas de Campaña**: Consulta métricas calculadas
- **Obtener Eventos de Campaña**: Lista eventos registrados
- **Obtener Métricas por Marca**: Métricas agrupadas por marca

### 🔄 Flujo Completo de Prueba
- Secuencia de peticiones que demuestra el flujo completo del sistema
- Incluye creación, inicio, registro de eventos y consulta de métricas

### 🧪 Casos de Prueba - Errores
- Pruebas de validación y manejo de errores
- Casos edge para verificar la robustez del sistema

## 🎯 Flujo de Prueba Recomendado

### 1. Verificación Inicial
```
🏥 Health Checks → Ejecutar toda la carpeta
```

### 2. Crear y Gestionar Campañas
```
📋 Afiliaciones Service → Crear Campaña
📋 Afiliaciones Service → Iniciar Campaña
📋 Afiliaciones Service → Obtener Campaña por ID
```

### 3. Registrar Eventos de Tracking
```
📊 Tracking Service → Registrar Evento - Vista
📊 Tracking Service → Registrar Evento - Clic
📊 Tracking Service → Registrar Evento - Conversión
📊 Tracking Service → Registrar Evento - Engagement
```

### 4. Consultar Métricas y Eventos
```
📊 Tracking Service → Obtener Métricas de Campaña
📊 Tracking Service → Obtener Eventos de Campaña
📊 Tracking Service → Obtener Métricas por Marca
```

### 5. Flujo Automatizado
```
🔄 Flujo Completo de Prueba → Ejecutar toda la carpeta
```

## 🔧 Variables de Entorno

La colección incluye las siguientes variables:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `base_url_afiliaciones` | http://localhost:8001 | URL del servicio de Afiliaciones |
| `base_url_marca` | http://localhost:8002 | URL del servicio de Marca |
| `base_url_influencer` | http://localhost:8003 | URL del servicio de Influencer |
| `base_url_tracking` | http://localhost:8004 | URL del servicio de Tracking |
| `marca_id` | 123e4567-e89b-12d3-a456-426614174000 | ID de marca para pruebas |
| `campana_id` | (se genera automáticamente) | ID de campaña creada |

## 🎨 Características de la Colección

### Scripts Automáticos
- **Pre-request Script**: Genera IDs únicos y timestamps
- **Test Script**: Extrae IDs de respuestas y hace logging

### Validaciones Automáticas
- Verificación de códigos de estado HTTP
- Extracción automática de IDs de campaña
- Logging de respuestas para debugging

### Datos de Prueba Realistas
- IDs de UUID válidos
- Timestamps actuales
- Datos de eventos variados y realistas

## 🐛 Debugging

### Ver Logs de los Servicios
```bash
# Logs de todos los servicios
make logs

# Logs de un servicio específico
make logs-afiliaciones
make logs-marca
make logs-influencer
make logs-tracking
```

### Verificar Estado de los Servicios
```bash
make status
```

### Reiniciar Servicios
```bash
make restart
```

## 📊 Monitoreo

### Pulsar Admin
- URL: http://localhost:8080
- Verifica que los eventos se estén publicando y consumiendo correctamente

### Documentación de APIs
- Afiliaciones: http://localhost:8001/docs
- Marca: http://localhost:8002/docs
- Influencer: http://localhost:8003/docs
- Tracking: http://localhost:8004/docs

## 🔍 Casos de Prueba Específicos

### Prueba de Eventos Asíncronos
1. Crear una campaña
2. Verificar en los logs que los servicios de Marca e Influencer procesaron el evento
3. Registrar eventos de tracking
4. Verificar que las métricas se actualizaron

### Prueba de Resiliencia
1. Ejecutar "Casos de Prueba - Errores"
2. Verificar que los errores se manejan correctamente
3. Confirmar que el sistema sigue funcionando después de errores

### Prueba de Performance
1. Crear múltiples campañas
2. Registrar muchos eventos de tracking
3. Verificar que las consultas de métricas siguen siendo rápidas

## 🚨 Solución de Problemas

### Servicios No Responden
```bash
# Verificar que Docker esté corriendo
docker ps

# Reiniciar servicios
make restart

# Ver logs de errores
make logs
```

### Eventos No Se Procesan
1. Verificar que Pulsar esté funcionando: http://localhost:8080
2. Revisar logs de consumidores
3. Verificar conectividad de red entre servicios

### Errores de Base de Datos
1. Verificar que las bases de datos estén corriendo
2. Revisar logs de conexión
3. Verificar variables de entorno

## 📈 Métricas de Prueba

La colección incluye ejemplos de diferentes tipos de eventos:

- **Vistas**: Simulan visualizaciones de contenido
- **Clics**: Simulan interacciones con elementos
- **Conversiones**: Simulan compras o acciones objetivo
- **Engagement**: Simulan likes, comentarios, etc.
- **Compartir**: Simulan compartir contenido
- **Comentarios**: Simulan interacciones de texto

Cada evento incluye datos contextuales realistas para probar el procesamiento completo del sistema.
