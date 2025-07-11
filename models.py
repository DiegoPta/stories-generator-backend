"""Definición de los modelos de datos para la API"""

# Python imports.
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class StoryRequest(BaseModel):
    """Modelo de solicitud para generar una historia"""

    word_count: int = Field(
        ..., ge=50, le=2000, description="Número de palabras para la historia"
    )
    creativity_level: str = Field(
        ...,
        pattern="^(conservador|creativo|locura)$",
        description="Nivel de creatividad",
    )
    genre: str = Field(
        ...,
        pattern="^(fantasia|ciencia_ficcion|misterio|romance|aventura|terror|comedia|drama)$",
        description="Género literario",
    )
    category: str = Field(
        ...,
        pattern="^(todos|adolescente|infantil)$",
        description="Categoría de la historia",
    )
    suggestions: Optional[str] = Field(
        None, description="Sugerencias adicionales para la historia"
    )


class StoryResponse(BaseModel):
    """Modelo de respuesta para la historia generada"""

    story: str = Field(..., description="La historia generada")
    metadata: Dict[str, Any] = Field(..., description="Metadatos de la generación")

    class Config:
        json_schema_extra = {
            "example": {
                "story": "Había una vez un dragón que...",
                "metadata": {
                    "word_count": 300,
                    "genre": "fantasía",
                    "category": "infantil",
                    "creativity_level": 0.8,
                    "generated_at": "2024-06-07T12:35:10.123Z",
                    "processing_time": 1.23,
                    "model": "openai_model_configurado",
                },
            }
        }


class RootResponse(BaseModel):
    """Modelo de respuesta para la raíz de la API"""

    message: str = Field(..., description="Mensaje de bienvenida de la API")
    version: str = Field(..., description="Versión actual de la API")
    model: str = Field(..., description="Modelo de IA configurado")
    endpoints: Dict[str, str] = Field(
        ..., description="Diccionario con los endpoints disponibles"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Generador de Historias API",
                "version": "1.0.0",
                "model": "openai_model_configurado",
                "endpoints": {
                    "root": "/",
                    "generate_story": "/generate-story",
                    "health": "/health",
                },
            }
        }


class HealthResponse(BaseModel):
    """Modelo de respuesta para la salud de la API"""

    status: str = Field(..., description="Estado general de la API")
    openai_status: str = Field(..., description="Estado de la conexión con OpenAI")
    timestamp: str = Field(..., description="Marca de tiempo de la verificación")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "openai_status": "connected",
                "timestamp": "2024-06-07T12:34:56.789Z",
            }
        }
