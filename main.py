"""Implementación de la API para generar historias únicas usando OpenAI GPT-4o-mini"""

# Python imports.
import time
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

# Project imports.
from models import StoryRequest, StoryResponse, RootResponse, HealthResponse
from services import generate_story_with_llm
from config import settings

# Configuración de logging.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de FastAPI.
app = FastAPI(
    title="Generador de Historias API",
    description="API para generar historias únicas usando OpenAI GPT-4o-mini",
    version="1.0.0",
)

# Configuración de CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> RootResponse:
    """
    Endpoint raíz de la API.
    Devuelve información básica sobre la API, incluyendo nombre, versión, modelo utilizado
    y los endpoints disponibles.
    """
    return RootResponse(
        message="Generador de Historias API",
        version="1.0.0",
        model=settings.openai_model,
        endpoints={
            "root": "/",
            "docs": "/docs",
            "generate_story": "/generate-story",
            "health": "/health",
        },
    )


@app.get("/health")
async def health_check() -> HealthResponse:
    """
    Endpoint de salud de la API.
    Verifica el estado general de la API y la configuración de OpenAI.
    - **openai_status**: Puede ser "connected", "not_configured" o "error".
    """
    try:
        # Validar configuración de OpenAI
        settings.validate_openai_config()
        openai_status = "connected"
    except ValueError:
        openai_status = "not_configured"
    except Exception:
        openai_status = "error"

    return HealthResponse(
        status="healthy",
        openai_status=openai_status,
        timestamp=datetime.utcnow().isoformat(),
    )


@app.post("/generate-story")
async def generate_story(request: StoryRequest) -> StoryResponse:
    """
    Genera una historia única usando los parámetros proporcionados en el cuerpo de la solicitud.
    Utiliza un modelo de lenguaje (por ejemplo, OpenAI GPT-4o-mini).

    Parámetros:
    - **request (StoryRequest)**: Objeto con los parámetros de generación de la historia.
        - **word_count (int)**: Cantidad de palabras deseadas.
        - **genre (str)**: Género de la historia.
        - **category (str)**: Categoría de la historia.
        - **creativity_level (float)**: Nivel de creatividad del modelo.

    Errores:
        400: Error de validación de los datos de entrada.
        500: Error interno al generar la historia.
    """
    start_time = time.time()
    logger.info(
        "Recibida solicitud:"
        f"word_count={request.word_count}, "
        f"genre={request.genre}, "
        f"creativity_level={request.creativity_level}, "
        f"category={request.category}"
    )

    try:
        story = await generate_story_with_llm(request)
        processing_time = time.time() - start_time

        response_data = StoryResponse(
            story=story,
            metadata={
                "word_count": request.word_count,
                "genre": request.genre,
                "category": request.category,
                "creativity_level": request.creativity_level,
                "generated_at": datetime.utcnow().isoformat(),
                "processing_time": round(processing_time, 2),
                "model": settings.openai_model,
            },
        )

        logger.info(f"Historia generada exitosamente en {processing_time:.2f}s")
        return response_data

    except ValidationError as ve:
        logger.error(f"Error de validación: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error al generar historia: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.host, port=settings.port)
