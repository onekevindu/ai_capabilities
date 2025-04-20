from fastapi import APIRouter, HTTPException
from app.schemas.launch import LaunchRequest
from app.schemas.model_schema import ModelConfig, ModelType
from app.services.model_service import model_service
from app.services.model_launcher import model_launcher

router = APIRouter(tags=["Launcher"])

@router.post("/launch")
async def launch_endpoint(req: LaunchRequest):
    try:
        # 创建模型配置
        model_config = ModelConfig(
            model_type=ModelType(req.task),
            model_id=req.repo or req.name,
            model_name=req.name,
            description=f"{req.task} model {req.name}"
        )
        
        # 注册模型
        model = model_service.register_model(model_config)
        
        # 启动模型
        launched_model = await model_launcher.launch_model(model.model_id)
        
        return {
            "success": True,
            "message": "Model launched successfully",
            "url": launched_model.url,
            "port": launched_model.port
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))