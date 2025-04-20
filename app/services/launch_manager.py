"""
长时间驻留的 Launch Manager：负责下载模型、构造 Runner、
创建子 FastAPI 应用并持久保存。
"""
from typing import Dict
from fastapi import FastAPI

from app.models import (
    llm_runner,
    ocr_runner,
    det_runner,
    asr_runner,
    tts_runner,
)

_TASK2RUNNER = {
    "llm": llm_runner.LLMRunner,
    "ocr": ocr_runner.OCRRunner,
    "det": det_runner.DETRunner,
    "asr": asr_runner.ASRRunner,
    "tts": tts_runner.TTSRunner,
}

class _LaunchManager:
    def __init__(self):
        # name → {"prefix": str, "app": FastAPI, "url": str}
        self.subapps: Dict[str, Dict] = {}

    async def launch(self, task: str, name: str, repo: str | None) -> str:
        if task not in _TASK2RUNNER:
            raise ValueError(f"Unsupported task {task}")
        if name in self.subapps:
            return self.subapps[name]["url"]

        runner_cls = _TASK2RUNNER[task]
        runner = runner_cls()
        await runner.init_model(repo)

        sub_app = FastAPI(title=f"{task}-{name}")
        sub_app.add_api_route(
            "/infer",
            runner.infer,
            methods=["POST"],
            summary=f"{task} inference",
        )

        prefix = f"/{task}/{name}"
        self.subapps[name] = {
            "prefix": prefix,
            "app": sub_app,
            "url": f"{prefix}/infer",
        }
        return self.subapps[name]["url"]

launch_manager = _LaunchManager()