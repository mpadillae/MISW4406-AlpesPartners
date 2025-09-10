from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from api.endpoints import router as tracking_router
from infraestructura.consumidores import iniciar_consumidores

app = FastAPI(
    title="Tracking Service",
    description="Microservicio de Tracking para métricas y seguimiento de campañas",
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

# Incluir routers
app.include_router(tracking_router, prefix="/tracking", tags=["tracking"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "tracking"}


@app.on_event("startup")
async def startup_event():
    # Iniciar consumidores de eventos
    await iniciar_consumidores()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
