import base64, asyncio
from whispercpp import Whisper
from app.models.base import BaseRunner


class ASRRunner(BaseRunner):
    async def init_model(self, repo: str | None):
        self.asr = Whisper(model=repo or "ggml-large.bin")

    async def infer(self, body: dict):
        wav_b64 = body.get("audio")
        if not wav_b64:
            return {"error": "audio field is required"}
        audio_bytes = base64.b64decode(wav_b64)
        text = await asyncio.get_event_loop().run_in_executor(None, self.asr.transcribe, audio_bytes)
        return {"text": text}