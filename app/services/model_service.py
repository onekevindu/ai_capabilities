import os
from typing import Dict, Optional
from fastapi import HTTPException
from app.schemas.model_schema import ModelConfig, ModelType

class ModelService:
    def __init__(self):
        self.models: Dict[str, ModelConfig] = {}
        self.port_counter = 8000
    
    def register_model(self, config: ModelConfig) -> ModelConfig:
        if config.model_id in self.models:
            raise HTTPException(status_code=400, detail=f"Model {config.model_id} already exists")
        
        config.port = self._get_next_port()
        config.url = f"http://localhost:{config.port}"
        self.models[config.model_id] = config
        return config
    
    def get_model(self, model_id: str) -> Optional[ModelConfig]:
        return self.models.get(model_id)
    
    def list_models(self, model_type: Optional[ModelType] = None) -> Dict[str, ModelConfig]:
        if model_type:
            return {k: v for k, v in self.models.items() if v.model_type == model_type}
        return self.models
    
    def _get_next_port(self) -> int:
        port = self.port_counter
        self.port_counter += 1
        return port

model_service = ModelService()