from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.launch_controller import router as launch_router
from app.services.launch_manager import launch_manager

app = FastAPI(
    title="Universal‑AI‑Hub",
    version="0.1.0",
    description="A platform for managing and launching various AI models",
)

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 业务路由
app.include_router(launch_router)

# 启动时把动态模型子应用挂载进来
@app.on_event("startup")
async def _mount_subapps():
    for sub in launch_manager.subapps.values():
        app.mount(sub["prefix"], sub["app"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8100, reload=True)