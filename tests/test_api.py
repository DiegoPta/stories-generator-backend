"""
Pruebas unitarias para la API de Generador de Historias.
Se utiliza pytest como runner y utilidades de unittest.mock para simular dependencias.
Cada método de la clase prueba un endpoint o caso relevante.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app


class TestAPI:
    """
    Pruebas para los endpoints principales de la API de Generador de Historias.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        """
        Fixture de setup para posibles configuraciones futuras.
        """
        pass

    def test_root(self):
        """
        Prueba el endpoint raíz `/` y verifica la estructura básica de la respuesta.
        """
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "model" in data
        assert "endpoints" in data

    def test_health(self):
        """
        Prueba el endpoint `/health` y verifica que el estado sea 'healthy'.
        """
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "openai_status" in data
        assert "timestamp" in data

    @patch("main.generate_story_with_llm", return_value="Había una vez un dragón...")
    def test_generate_story_success(self, mock_generate):
        """
        Prueba el endpoint `/generate-story` con datos válidos y verifica la respuesta.
        """
        payload = {
            "word_count": 300,
            "creativity_level": "creativo",
            "genre": "fantasia",
            "category": "infantil"
        }
        client = TestClient(app)
        response = client.post("/generate-story", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "story" in data
        assert data["story"] == "Había una vez un dragón..."
        assert "metadata" in data
        assert data["metadata"]["word_count"] == 300
        assert data["metadata"]["genre"] == "fantasia"
        assert data["metadata"]["category"] == "infantil"
        assert (
            data["metadata"]["creativity_level"] == "creativo"
            or data["metadata"]["creativity_level"] == "creativo"
        )

    def test_generate_story_validation_error(self):
        """
        Prueba el endpoint `/generate-story` con datos inválidos y espera un error 400 o 422.
        """
        payload = {
            "word_count": 10,  # Menor al mínimo permitido
            "creativity_level": "creativo",
            "genre": "fantasia",
            "category": "infantil",
        }
        client = TestClient(app)
        response = client.post("/generate-story", json=payload)
        assert response.status_code == 422 or response.status_code == 400
