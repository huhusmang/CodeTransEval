# main.py
import json
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()


class Params(BaseModel):
    python: Dict[str, List[str]]
    java: Dict[str, List[str]]
    cpp: Dict[str, List[str]]


class FuncData(BaseModel):
    id: int
    tag: str
    difficulty: str
    url: str
    entry_point: str
    params: Params
    python: str
    java: str
    cpp: str


class SecData(BaseModel):
    ID: str
    CWE: str
    Description: str
    VulCode: str
    Source: str


@router.get("/functiondata")
async def read_func_data():
    # Replace this with actual data fetching logic
    with open("/home/huhu/work/CodeTransSecEval/datas/function/datas.json") as f:
        data = json.load(f)
    return data


@router.get("/securitydata")
async def read_sec_data():
    # Replace this with actual data fetching logic
    with open("/home/huhu/work/CodeTransSecEval/datas/security/datas.json") as f:
        data = json.load(f)
    return data
