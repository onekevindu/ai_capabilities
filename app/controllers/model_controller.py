from fastapi import APIRouter, HTTPException
from typing import Dict, Optional, List
from app.schemas.model_schema import ModelConfig, ModelType, ModelResponse
from app.schemas.response_schema import APIResponse
from app.services.model_service import model_service
from app.services.model_launcher import model_launcher

router = APIRouter(prefix="/api/models", tags=["models"])

@router.post("/register", response_model=APIResponse[ModelConfig])
async def register_model(config: ModelConfig):
    try:
        model = model_service.register_model(config)
        return APIResponse(data=model)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/list", response_model=APIResponse[List[ModelConfig]])
async def list_models(model_type: Optional[ModelType] = None):
    models = model_service.list_models(model_type)
    return APIResponse(data=list(models.values()))

@router.post("/launch/{model_id}", response_model=APIResponse[ModelResponse])
async def launch_model(model_id: str):
    try:
        model = await model_launcher.launch_model(model_id)
        response = ModelResponse(
            success=True,
            message="Model launched successfully",
            url=model.url,
            port=model.port
        )
        return APIResponse(data=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop/{model_id}", response_model=APIResponse[ModelResponse])
async def stop_model(model_id: str):
    try:
        await model_launcher.stop_model(model_id)
        response = ModelResponse(
            success=True,
            message="Model stopped successfully"
        )
        return APIResponse(data=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))