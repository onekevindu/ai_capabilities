from typing import Literal, Optional
from pydantic import BaseModel, Field

class LaunchRequest(BaseModel):
    task: Literal["llm", "ocr", "det", "asr", "tts"] = Field(..., description="任务类型")
    name: str = Field(..., description="实例化后用于路由前缀的名称")
    repo: Optional[str] = Field(None, description="Hugging Face Repo ID 或权重地址")