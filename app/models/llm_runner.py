import asyncio
from typing import List

from pydantic import BaseModel
from vllm import LLM, SamplingParams
from app.models.base import BaseRunner


class _Message(BaseModel):
    role: str
    content: str


class _InferBody(BaseModel):
    messages: List[_Message]


class LLMRunner(BaseRunner):
    async def init_model(self, repo: str | None):
        repo = repo or "Qwen/Qwen1.5-7B-Chat"
        self.sampling_params = SamplingParams(temperature=0.7, top_p=0.9)
        self.model = LLM(model=repo)

    async def infer(self, body: dict):
        data = _InferBody(**body)
        msgs = [{"role": m.role, "content": m.content} for m in data.messages]
        text = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.model.generate(msgs, self.sampling_params)[0].outputs[0].text,
        )
        return {"text": text.strip()}