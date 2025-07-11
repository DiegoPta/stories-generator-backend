"""Servicios para la API"""

# Python imports.
import openai
import logging

# Project imports.
from models import StoryRequest
from prompt_manager import prompt_manager
from config import settings

# Configuración de logging.
logger = logging.getLogger(__name__)


# Genera una historia usando OpenAI GPT-4o-mini con prompts dinámicos.
async def generate_story_with_llm(request: StoryRequest) -> str:
    """
    Genera una historia usando OpenAI GPT-4o-mini con prompts dinámicos
    """
    try:
        # Validar configuración de OpenAI
        settings.validate_openai_config()

        # Configurar OpenAI client (solo cuando se necesita)
        client = openai.OpenAI(api_key=settings.openai_api_key)

        # Generar el prompt usando el gestor de plantillas
        prompt = prompt_manager.generate_prompt(request)

        # Logging específico de los parámetros
        logger.info("PARÁMETROS DEL REQUEST:")
        logger.info(f"  - word_count: {request.word_count}")
        logger.info(f"  - creativity_level: {request.creativity_level}")
        logger.info(f"  - genre: {request.genre}")
        logger.info(f"  - category: {request.category}")
        logger.info(f"  - suggestions: {request.suggestions or 'Ninguna'}")
        logger.info("=" * 80)

        # Llamar a OpenAI usando la nueva sintaxis
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un escritor creativo experto en narrativa. "
                        "Responde solo con la historia solicitada, sin "
                        "introducciones ni explicaciones adicionales."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=settings.openai_max_tokens,
            temperature=settings.openai_temperature,
            top_p=0.9,
            frequency_penalty=0.1,
            presence_penalty=0.1,
        )

        # Extraer la historia de la respuesta
        content = response.choices[0].message.content
        if content is None:
            raise Exception("OpenAI no generó contenido en la respuesta")

        story = content.strip()

        logger.info(f"Historia generada exitosamente con {len(story.split())} palabras")

        return story

    except openai.AuthenticationError:
        logger.error("Error de autenticación con OpenAI - Verifica tu API key")
        raise Exception("Error de autenticación con OpenAI. Verifica tu API key.")

    except openai.RateLimitError:
        logger.error("Límite de velocidad excedido en OpenAI")
        raise Exception(
            "Límite de velocidad excedido. Intenta de nuevo en unos momentos."
        )

    except openai.APIError as e:
        logger.error(f"Error de API de OpenAI: {e}")
        raise Exception(f"Error en el servicio de OpenAI: {str(e)}")

    except Exception as e:
        logger.error(f"Error inesperado al generar historia: {e}")
        raise Exception(f"Error inesperado al generar la historia: {str(e)}")
