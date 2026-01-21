import httpx
from app.models.all import Model

class LLMService:
    def __init__(self):
        self.timeout = httpx.Timeout(60.0, connect=5.0)

    async def generate_response(self, model: Model, messages: list[dict]) -> str:
        """
        Generic handler that assumes an OpenAI-compatible API structure 
        (which Ollama and vLLM support via /v1/chat/completions).
        """
        url = f"{model.api_base_url}/v1/chat/completions"
        if "ollama" in model.api_base_url:
            # Ollama specific tweaks if needed, but usually v1 compatible
             url = f"{model.api_base_url}/api/chat"

        # Preparing payload based on provider if we strictly support Ollama native API
        # but let's assume we want to use the standard openai-compatible endpoint of Ollama if possible
        # For this example, let's implement the specific Ollama /api/chat format to be safe as per "self-hosted" requirement
        
        payload = {
            "model": model.model_key,
            "messages": messages,
            "stream": False 
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                
                # Check format
                if "message" in data:
                     return data["message"]["content"]
                # Fallback for openai format
                if "choices" in data:
                    return data["choices"][0]["message"]["content"]
                    
                return "Error: Unexpected response format from LLM provider."
            except httpx.HTTPError as e:
                return f"Error communicating with LLM: {str(e)}"
