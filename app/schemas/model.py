from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ModelBase(BaseModel):
    name: str
    api_base_url: str
    model_key: str

class ModelCreate(ModelBase):
    pass

class ModelResponse(ModelBase):
    id: UUID

    class Config:
        from_attributes = True