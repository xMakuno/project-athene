from fastapi import APIRouter, Depends, HTTPException
from app.services.llm_service import LLMService
from app.schemas.summary import SummaryRequest, SummaryResponse

router = APIRouter()

async def get_llm_service()->LLMService:
    return LLMService()
@router.post("/") # response_model=SummaryResponse)
async def generate_summary(request: SummaryRequest, service: LLMService = Depends(get_llm_service)):
    try:
        response_data = await service.send_prompt(request.prompt)
        print(response_data)
        if not response_data:
            raise HTTPException(status_code=500, detail="Empty response from LLM")

        return response_data["choices"][0]["message"]
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/extract")
async def extract_information(request: SummaryRequest, service: LLMService = Depends(get_llm_service)):
    try:
        response_data = await service.send_prompt(request.prompt)
        return response_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))