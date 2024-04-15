from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import evaluate, data, prediction, analyze

app = FastAPI()

app.include_router(evaluate.router)
app.include_router(data.router)
app.include_router(prediction.router)
app.include_router(analyze.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源列表
    allow_credentials=True,  # 允许携带cookie
    allow_methods=["*"],  # 允许的HTTP方法
    allow_headers=["*"],  # 允许的HTTP头
)
