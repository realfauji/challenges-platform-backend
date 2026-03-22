from pydantic import BaseModel, Field


class CreateChallenge(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    target_value: int = Field(default=0)
    duration_days: int = Field(...)
    is_active: bool = Field(default=True)

class UpdateProgress(BaseModel):
    challenge_id: str = Field(...)
    progress_value: int = Field(...)
    
