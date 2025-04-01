from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from app.schemas.response_schema import APIResponse
from app.models.hello_model import HelloWorld
router = APIRouter()

@router.get("/hello", response_model=APIResponse[str])
async def get_hello():
    hello = HelloWorld.generate_hello()
    return APIResponse(data=hello)

@router.post("/hello", response_model=APIResponse[str])
async def create_item():
    hello = HelloWorld.generate_hello()
    return APIResponse(data=hello)
