from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from api.endpoints import router as afiliaciones_router

app = FastAPI(
    title="Afiliaciones Service",
    description="Microservicio de Afiliaciones para gestión de campañas",
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
app.include_router(afiliaciones_router,
                   prefix="/afiliaciones", tags=["afiliaciones"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "afiliaciones"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
