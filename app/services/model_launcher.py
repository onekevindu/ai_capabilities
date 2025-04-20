import subprocess
from typing import Optional
from fastapi import HTTPException
from app.schemas.model_schema import ModelConfig, ModelType
from app.services.model_service import model_service

class ModelLauncher:
    def __init__(self):
        self.running_processes = {}
    
    async def launch_model(self, model_id: str) -> ModelConfig:
        model = model_service.get_model(model_id)
        if not model:
            raise HTTPException(status_code=404, detail=f"Model {model_id} not found")
        
        if model_id in self.running_processes:
            return model
        
        try:
            if model.model_type == ModelType.LLM:
                await self._launch_llm(model)
            elif model.model_type == ModelType.OCR:
                await self._launch_ocr(model)
            elif model.model_type == ModelType.ASR:
                await self._launch_asr(model)
            elif model.model_type == ModelType.TTS:
                await self._launch_tts(model)
            elif model.model_type == ModelType.DETECTION:
                await self._launch_detection(model)
            
            model.status = "running"
            return model
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def _launch_llm(self, model: ModelConfig):
        cmd = [
            "python", "-m", "vllm.entrypoints.api_server",
            "--model", model.model_id,
            "--port", str(model.port)
        ]
        self._start_process(model.model_id, cmd)
    
    async def _launch_ocr(self, model: ModelConfig):
        # 实现OCR模型启动逻辑
        pass
    
    async def _launch_asr(self, model: ModelConfig):
        # 实现ASR模型启动逻辑
        pass
    
    async def _launch_tts(self, model: ModelConfig):
        # 实现TTS模型启动逻辑
        pass
    
    async def _launch_detection(self, model: ModelConfig):
        # 实现目标检测模型启动逻辑
        pass
    
    def _start_process(self, model_id: str, cmd: list):
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.running_processes[model_id] = process
    
    async def stop_model(self, model_id: str):
        if model_id in self.running_processes:
            process = self.running_processes[model_id]
            process.terminate()
            process.wait()
            del self.running_processes[model_id]
            
            model = model_service.get_model(model_id)
            if model:
                model.status = "stopped"

model_launcher = ModelLauncher()