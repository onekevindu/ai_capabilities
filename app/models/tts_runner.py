import base64, tempfile, asyncio
from TTS.api import TTS
from app.models.base import BaseRunner


class TTSRunner(BaseRunner):
    async def init_model(self, repo: str | None):
        self.tts = TTS(model_name=repo or "tts_models/zh-CN/baker")

    async def infer(self, body: dict):
        text = body.get("text", "")
        if not text:
            return {"error": "text field is required"}
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            await asyncio.get_event_loop().run_in_executor(None, self.tts.tts_to_file, text, f.name)
            f.seek(0)
            data = base64.b64encode(f.read()).decode()
        return {"audio": data, "format": "wav"}