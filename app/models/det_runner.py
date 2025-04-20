import base64, io, asyncio
from ultralytics import YOLO
from PIL import Image
from app.models.base import BaseRunner


class DETRunner(BaseRunner):
    async def init_model(self, repo: str | None):
        self.det = YOLO(repo or "yolov8s.pt")

    async def infer(self, body: dict):
        img_b64 = body.get("image")
        if not img_b64:
            return {"error": "image field is required"}
        img = Image.open(io.BytesIO(base64.b64decode(img_b64)))
        dets = await asyncio.get_event_loop().run_in_executor(None, self.det, img)
        boxes = [
            {"cls": int(b.cls), "conf": float(b.conf), "xyxy": [float(x) for x in b.xyxy[0]]}
            for b in dets[0].boxes
        ]
        return {"boxes": boxes}