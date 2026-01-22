from fastapi import APIRouter, Depends, HTTPException
from app.services.llm_service import LLMService
from app.schemas.summary import SummaryRequest, SummaryResponse

router = APIRouter()

async def get_llm_service()->LLMService:
    return LLMService()
@router.post("/") # response_model=SummaryResponse)
async def generate_summary(request: SummaryRequest, service: LLMService = Depends(get_llm_service)):
    try:
        response_data = await service.generate_summary(request.prompt)
        # Extract content from OpenAI-compatible response
        """ if "choices" in response_data and len(response_data["choices"]) > 0:
            summary_text = response_data["choices"][0]["message"]["content"]
            return SummaryResponse(summary=summary_text) """
        return response_data
        else:
            raise ValueError("Unexpected response format from LLM")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))