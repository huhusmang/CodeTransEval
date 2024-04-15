import json
from fastapi import APIRouter


router = APIRouter()


@router.get("/results")
async def read_func_data():
    # Replace this with actual data fetching logic
    with open("/home/huhu/work/CodeTransSecEval/datas/function/predictions/results.json") as f:
        data = json.load(f)
    return data