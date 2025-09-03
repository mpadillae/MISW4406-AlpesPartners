# Tutorial 5 - CQRS y manejo de eventos

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&repo=MISW4406/tutorial-5-cqrs-eventos)

Repositorio con código base para el uso de un sistema usando el patrón CQRS y usando eventos de dominio e integración para la comunicación asíncrona entre componentes internos parte del mismo contexto acotado y sistemas externos.

Este repositorio está basado en el repositorio de sidecars visto en el tutorial 4 del curso. Por tal motivo, puede usar ese mismo repositorio para entender algunos detalles que este README no cubre.

## Arquitectura

<img width="3228" height="387" alt="5" src="https://github.com/user-attachments/assets/673a55e4-4d0b-47f7-baad-42a85d89b64d" />

## Estructura del proyecto

Este repositorio sigue en general la misma estructura del repositorio de origen. Sin embargo, hay un par de adiciones importante mencionar:

- El directorio **src** ahora cuenta con un nuevo directorio llamado **notificaciones**, el cual representa un servicio de mensajería que recibe eventos de integración propagados del sistema de AlpesPartners, por medio de un broker de eventos.
- El directorio **src** ahora también cuenta cuenta con un nuevo directorio llamado **ui**, el cual representa nuestra interfaz gráfica la cual puede recibir por medio de un BFF desarrollado en Python usando websockets, las respuestas de nuestros comandos de forma asíncrona.
- Nuestro proyecto de AlpesPartners ha cambiado de forma considerable. Los siguientes son los cambios relevantes en cada módulo:
  - **api**: En este módulo se modificó el API de `vuelos.py` el cual cuenta con dos nuevos endpoints: `/reserva-commando` y `/reserva-query`, los cuales por detrás de escenas usan un patrón CQRS como la base de su comunicación.
  - **modulos/../aplicacion**: Este módulo ahora considera los sub-módulos: `queries` y `comandos`. En dichos directorios pdrá ver como se desacopló las diferentes operaciones lectura y escritura. Vea en el módulo `vuelos` los archivos `obtener_reserva.py` y `crear_reserva.py` para ver como se logra dicho desacoplamiento.
  - **modulos/../aplicacion/handlers.py**: Estos son los handlers de aplicación que se encargan de oir y reaccionar a eventos. Si consulta el módulo de clientes podra ver que tenemos handlers para oir y reaccionar a los eventos de dominio para poder continuar con una transacción. En el modulo de vuelos encontramos handlers para eventos de integración los cuales pueden ser disparados desde la capa de infraestructura, la cual está consumiendo eventos y comandos del broker de eventos.
  - **modulos/../dominio/eventos.py**: Este archivo contiene todos los eventos de dominio que son disparados cuando una actividad de dominio es ejecutada de forma correcta.
  - **modulos/../infraestructura/consumidores.py**: Este archivo cuenta con toda la lógica en términos de infrastructura para consumir los eventos y comandos que provienen del broker de eventos. Desarrollado de una forma funcional.
  - **modulos/../infraestructura/despachadores.py**: Este archivo cuenta con toda la lógica en terminos de infrastructura para publicar los eventos y comandos de integración en el broker de eventos. Desarrollado de manera OOP.
  - **modulos/../infraestructura/schema**: En este directorio encontramos la definición de los eventos y comandos de integración. Puede ver que se usa un formato popular en la comunidad de desarrollo de software open source, en donde los directorios/módulos nos dan un indicio de las versiones `/schema/v1/...`. De esta manera podemos estar tranquilos con versiones incrementales y menores, pero listos cuando tengamos que hacer un cambio grande.
  - **seedwork/aplicacion/comandos.py**: Definición general de los comandos, handlers e interface del despachador.
  - **seedwork/infraestructura/queries.py**: Definición general de los queries, handlers e interface del despachador.
  - **seedwork/infraestructura/uow.py**: La Unidad de Trabajo (UoW) mantiene una lista de objetos afectados por una transacción de negocio y coordina los cambios de escritura. Este objeto nos va ser de gran importancia, pues cuando comenzamos a usar eventos de dominio e interactuar con otros módulos, debemos ser capaces de garantizar consistencia entre los diferentes objetos y partes de nuestro sistema.

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
