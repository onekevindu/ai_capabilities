import base64, io, asyncio
from paddleocr import PaddleOCR
from PIL import Image
from app.models.base import BaseRunner


class OCRRunner(BaseRunner):
    async def init_model(self, repo: str | None):
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")

    async def infer(self, body: dict):
        img_b64 = body.get("image")
        if not img_b64:
            return {"error": "image field is required"}
        img = Image.open(io.BytesIO(base64.b64decode(img_b64)))
        result = await asyncio.get_event_loop().run_in_executor(None, self.ocr.ocr, img)
        text = "\n".join([line[1][0] for line in result[0]])
        return {"text": text}