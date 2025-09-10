from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from infraestructura.consumidores import iniciar_consumidores

app = FastAPI(
    title="Marca Service",
    description="Microservicio de Marca para procesamiento de eventos de campañas",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "marca"}


@app.on_event("startup")
async def startup_event():
    # Iniciar consumidores de eventos
    await iniciar_consumidores()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
