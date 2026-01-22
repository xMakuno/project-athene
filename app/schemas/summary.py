from pydantic import BaseModel

class SummaryRequest(BaseModel):
    # TODO: implemente multiple llm
    # model_id: UUID 
    story: str

class SummaryResponse(BaseModel):
    summary: str