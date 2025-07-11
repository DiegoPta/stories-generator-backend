"""Gestor de prompts para la API"""

# Python imports.
import yaml
from typing import Dict, Any

# Project imports.
from models import StoryRequest


class PromptManager:
    """Clase gestora de prompts para la API"""

    def __init__(self, prompts_file: str = "prompts.yaml"):
        """Inicializa el gestor de prompts cargando el archivo YAML"""
        self.prompts_file = prompts_file
        self.prompts_data = self._load_prompts()

    def _load_prompts(self) -> Dict[str, Any]:
        """Carga las plantillas de prompts desde el archivo YAML"""
        try:
            with open(self.prompts_file, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"No se encontró el archivo de prompts: {self.prompts_file}"
            )
        except yaml.YAMLError as e:
            raise ValueError(f"Error al parsear el archivo YAML: {e}")

    def reload_prompts(self) -> None:
        """Recarga las plantillas de prompts desde el archivo"""
        self.prompts_data = self._load_prompts()

    def get_genre_info(self, genre: str) -> Dict[str, str]:
        """Obtiene la información específica de un género"""
        genres = self.prompts_data.get("genres", {})
        if genre not in genres:
            # Fallback a fantasía si el género no existe
            return genres.get("fantasia", {})
        return genres[genre]

    def get_creativity_info(self, creativity_level: str) -> Dict[str, str]:
        """Obtiene la información específica de un nivel de creatividad"""
        creativity_levels = self.prompts_data.get("creativity_levels", {})
        if creativity_level not in creativity_levels:
            # Fallback a creativo si el nivel no existe
            return creativity_levels.get("creativo", {})
        return creativity_levels[creativity_level]

    def generate_prompt(self, request: StoryRequest) -> str:
        """Genera el prompt completo basado en el request"""
        # Obtener información del género y creatividad
        genre_info = self.get_genre_info(request.genre)
        creativity_info = self.get_creativity_info(request.creativity_level)

        # Primero formatear el base_prompt con los parámetros básicos
        base_prompt_params = {
            "genre": request.genre,
            "category": request.category,
            "word_count": request.word_count,
            "creativity_level": request.creativity_level,
            "suggestions": request.suggestions or "Ninguna sugerencia específica",
        }

        base_prompt_template = self.prompts_data.get("base_prompt", "")
        formatted_base_prompt = base_prompt_template.format(**base_prompt_params)

        # Preparar los parámetros para la plantilla final
        params = {
            "base_prompt": formatted_base_prompt,
            "genre": request.genre,
            "genre_description": genre_info.get("description", ""),
            "genre_elements": genre_info.get("elements", ""),
            "genre_tone": genre_info.get("tone", ""),
            "creativity_level": request.creativity_level,
            "creativity_instructions": creativity_info.get("instructions", ""),
        }

        # Generar el prompt final usando la plantilla
        prompt_template = self.prompts_data.get("prompt_template", "")

        try:
            final_prompt = prompt_template.format(**params)
            return final_prompt
        except KeyError as e:
            raise ValueError(f"Error en la plantilla de prompt: parámetro faltante {e}")

    def get_available_genres(self) -> list:
        """Retorna la lista de géneros disponibles"""
        return list(self.prompts_data.get("genres", {}).keys())

    def get_available_creativity_levels(self) -> list:
        """Retorna la lista de niveles de creatividad disponibles"""
        return list(self.prompts_data.get("creativity_levels", {}).keys())


# Instancia global del gestor de prompts
prompt_manager = PromptManager()
