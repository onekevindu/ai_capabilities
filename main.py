from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import hello_controller

app = FastAPI(
    title="FastAPI Project",
    description="A standard FastAPI project structure",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(hello_controller.router, prefix="/api", tags=["hello"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8100, reload=True)