import os
from typing import Optional
from dotenv import load_dotenv
import logging

# Configurar logging
logger = logging.getLogger(__name__)

# Cargar variables de entorno desde .env
logger.info("=" * 50)
logger.info("CARGANDO ARCHIVO .env:")
logger.info(f"Directorio actual: {os.getcwd()}")
logger.info(f"Archivo .env existe: {os.path.exists('.env')}")

# Intentar cargar .env
load_dotenv()

# Verificar variables después de cargar
logger.info("VARIABLES DE ENTORNO DESPUÉS DE CARGAR .env:")
logger.info(f"CORS_ORIGINS: '{os.getenv('CORS_ORIGINS')}'")
logger.info(
    f"OPENAI_API_KEY: {'Configurada' if os.getenv('OPENAI_API_KEY') else 'No configurada'}"
)
logger.info("=" * 50)


class Settings:
    """Configuración de la aplicación"""

    # OpenAI Configuration
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    openai_max_tokens: int = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
    openai_temperature: float = float(os.getenv("OPENAI_TEMPERATURE", "0.8"))

    # Server Configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))

    # CORS Configuration - Permitir todos los orígenes para desarrollo
    def _get_cors_origins(self) -> list:
        """Obtiene los orígenes CORS - permite todos para desarrollo"""
        cors_env = os.getenv("CORS_ORIGINS", "*")

        if cors_env == "*":
            # En desarrollo, permitir TODOS los orígenes
            result = ["*"]
            logger.info(f"CORS configurado para permitir todos: {result}")
            return result
        else:
            # Usar los orígenes específicos configurados
            result = [origin.strip() for origin in cors_env.split(",")]
            logger.info(f"CORS configurado con orígenes específicos: {result}")
            return result

    @property
    def cors_origins(self) -> list:
        """Obtiene los orígenes CORS"""
        return self._get_cors_origins()

    @classmethod
    def validate_openai_config(cls) -> bool:
        """Valida que la configuración de OpenAI esté completa"""
        if not cls.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY no está configurada. "
                "Por favor, establece la variable de entorno OPENAI_API_KEY"
            )
        return True


# Instancia global de configuración
settings = Settings()
