from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "Success"
    data: Optional[T] = None

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "Success",
                "data": None
            }
        }
