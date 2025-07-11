# Generador de Historias Backend

Este proyecto implementa el backend para el Generador de Historias usando FastAPI y OpenAI GPT-4o-mini, con un sistema de plantillas YAML para prompts dinámicos.

## 🚀 Instalación

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

1. **Configura tu API key de OpenAI:**
   Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
   ```bash
   OPENAI_API_KEY=tu_api_key_de_openai_aqui
   OPENAI_MODEL=gpt-4o-mini          # Modelo de OpenAI (default: gpt-4o-mini)
   OPENAI_MAX_TOKENS=2000            # Máximo de tokens (default: 2000)
   OPENAI_TEMPERATURE=0.8            # Temperatura de creatividad (default: 0.8)
   HOST=0.0.0.0                      # Host del servidor (default: 0.0.0.0)
   PORT=8000                         # Puerto del servidor (default: 8000)
   CORS_ORIGINS=http://localhost:3000 # Orígenes permitidos para CORS
   ```

## 🏁 Ejecución

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 Endpoints

### GET `/`
Información básica de la API y endpoints disponibles.

#### Response (200 OK)
```json
{
    "message": "Generador de Historias API",
    "version": "1.0.0",
    "model": "gpt-4o-mini",
    "endpoints": {
        "root": "/",
        "generate_story": "/generate-story",
        "health": "/health"
    }
}
```

### GET `/health`
Verifica el estado del backend y la conexión con OpenAI.

#### Response (200 OK)
```json
{
    "status": "healthy",
    "openai_status": "connected",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### POST `/generate-story`
Genera una historia usando OpenAI GPT-4o-mini con prompts dinámicos.

#### Request Body
```json
{
    "word_count": 300,
    "creativity_level": "creativo",
    "genre": "fantasia",
    "category": "infantil",
    "suggestions": "Un dragón en una montaña nevada"
}
```

#### Response (200 OK)
```json
{
    "story": "Érase una vez...",
    "metadata": {
        "word_count": 300,
        "genre": "fantasia",
        "category": "infantil",
        "creativity_level": "creativo",
        "generated_at": "2024-01-01T12:00:00Z",
        "processing_time": 2.5,
        "model": "gpt-4o-mini"
    }
}
```

### GET `/docs`
Documentación interactiva de la API (Swagger UI)

## 🎨 Plantillas de Prompts

El sistema usa plantillas YAML (`prompts.yaml`) que puedes editar fácilmente:

### Estructura de las Plantillas
- **Géneros**: Cada género tiene descripción, elementos típicos y tono
- **Niveles de Creatividad**: Instrucciones específicas para cada nivel
- **Prompt Base**: Instrucciones generales para el modelo
- **Plantilla Final**: Combina todos los elementos

### Ejemplo de Personalización
```yaml
genres:
  fantasia:
    description: "Tu descripción personalizada"
    elements: "tus elementos preferidos"
    tone: "tu tono deseado"
```

## 📦 Dependencias

### Principales
- fastapi
- uvicorn
- pydantic
- openai
- pyyaml
- python-dotenv

## 🔧 Características

- ✅ **Integración con OpenAI GPT-4o-mini**
- ✅ **Sistema de plantillas YAML dinámicas**
- ✅ **Validación de parámetros con Pydantic**
- ✅ **Manejo de errores robusto**
- ✅ **Logging detallado**
- ✅ **CORS configurado para desarrollo**
- ✅ **Tipado fuerte con modelos de respuesta**

## 🧪 Testing

### Con curl
```bash
curl -X POST "http://localhost:8000/generate-story" \
     -H "Content-Type: application/json" \
     -d '{
       "word_count": 300,
       "creativity_level": "creativo",
       "genre": "fantasia",
       "category": "infantil",
       "suggestions": "Un dragón en una montaña nevada"
     }'
```

### Con Python requests
```python
import requests

response = requests.post(
    "http://localhost:8000/generate-story",
    json={
        "word_count": 300,
        "creativity_level": "creativo",
        "genre": "fantasia",
        "category": "infantil",
        "suggestions": "Un dragón en una montaña nevada"
    }
)

print(response.json())
```

## 🔍 Debugging

### Verificar Estado
```bash
curl http://localhost:8000/health
```

## ⚠️ Consideraciones

1. **API Key**: Asegúrate de tener una API key válida de OpenAI en el archivo `.env`
2. **Costos**: Monitorea el uso de tokens para controlar costos
3. **Rate Limits**: Respeta los límites de velocidad de OpenAI
4. **Prompts**: Personaliza las plantillas según tus necesidades

## 🎯 Próximos Pasos

- [ ] Implementar cache de historias
- [ ] Agregar autenticación
- [ ] Métricas de uso
- [ ] Más géneros y niveles de creatividad
- [ ] Integración con otros modelos LLM 