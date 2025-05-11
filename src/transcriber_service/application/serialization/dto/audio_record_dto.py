from pydantic import BaseModel, Field
from datetime import datetime


class AudioRecordDTO(BaseModel):
    entity_type: str = Field(..., pattern="^(audio_record)$")
    id: str
    record_name: str
    file_path: str
    storage_id: str
    text: str | None = None
    language: str | None = None
    tags: list[str]
    last_updated: datetime

    class Config:
        from_attributes = True
