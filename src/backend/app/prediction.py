from pathlib import Path
from fastapi import APIRouter
import json


router = APIRouter()


@router.get("/models")
async def models():
    model_path = Path("/home/huhu/work/CodeTransSecEval/datas/function/predictions")
    models = []
    for model in model_path.iterdir():
        if model.is_dir():
            models.append(model.name)
    return models


@router.get("/predict")
async def predict(model: str, task: str):
    data_base_path = Path("/home/huhu/work/CodeTransSecEval/datas/function/predictions")
    data_path = data_base_path / model / task / "prediction.json"
    if not data_path.exists():
        return {"error": "Data not found"}
    with open(data_path) as f:
        datas = json.load(f)
    return datas
