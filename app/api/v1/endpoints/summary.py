from fastapi import APIRouter, Depends, HTTPException
from app.services.llm_service import LLMService
from app.schemas.summary import SummaryRequest, SummaryResponse

router = APIRouter()

async def get_llm_service()->LLMService:
    return LLMService()
@router.post("/", response_model=SummaryResponse)
async def generate_summary(request: SummaryRequest, service: LLMService = Depends(get_llm_service)):
    try:
        summary_text = await service.generate_summary(request.story)
        return SummaryResponse(summary=summary_text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))