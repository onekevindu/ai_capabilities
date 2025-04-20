from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class ModelType(str, Enum):
    LLM = "llm"
    OCR = "ocr"
    DETECTION = "detection"
    ASR = "asr"
    TTS = "tts"

class ModelConfig(BaseModel):
    model_type: ModelType
    model_id: str
    model_name: str
    description: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)
    port: Optional[int] = None
    url: Optional[str] = None
    status: str = "stopped"

class ModelResponse(BaseModel):
    success: bool
    message: str
    url: Optional[str] = None
    port: Optional[int] = None