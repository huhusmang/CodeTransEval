import subprocess
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class FuncItem(BaseModel):
    model: str
    task: str
    predictionCount: int


class SecItem(BaseModel):
    model: str


def run_command(command: str) -> dict:
    try:
        process = subprocess.Popen(command, shell=True)
        pid = process.pid + 1
        process.communicate()
    except subprocess.CalledProcessError as e:
        return {"task_id": pid, "status": "checkFailed"}

    return check_process_status(pid)


def check_process_status(pid: int) -> dict:
    try:
        subprocess.check_output(f"ps -p {pid}", shell=True)
        status = "running"
    except subprocess.CalledProcessError:
        status = "completed"

    return {"task_id": pid, "status": status}


@router.post("/funcgen")
async def funcgen(item: FuncItem):
    command = f"""
        nohup python3 /home/huhu/work/CodeTransSecEval/src/function_gen_prediction.py \
        --model_name {item.model} \
        --task {item.task} \
        --start 1 \
        --end 2 \
        --prediction_nums {item.predictionCount} \
        --is_save \
        > /home/huhu/work/CodeTransSecEval/datas/function/logs/temp/functionprediction.log 2>&1 &
    """
    return run_command(command)


@router.post("/funceval")
async def funceval(item: FuncItem):
    command = f"""
        nohup python3 /home/huhu/work/CodeTransSecEval/src/function_run_evaluation.py \
        --model_name {item.model} \
        --task {item.task} \
        --start 1 \
        --end 2 \
        --prediction_nums {item.predictionCount} 
        > /home/huhu/work/CodeTransSecEval/datas/function/logs/temp/functionevaluation.log 2>&1 &
    """
    return run_command(command)


@router.post("/secgen")
async def secgen(item: SecItem):
    command = f"""
        nohup python3 /home/huhu/work/CodeTransSecEval/src/security_gen_prediction.py \
        --model_name {item.model} \
        > /home/huhu/work/CodeTransSecEval/datas/function/logs/temp/securityprediction.log 2>&1 &
    """
    return run_command(command)


@router.post("/seceval")
async def seceval(item: SecItem):
    command = f"""
        nohup python3 /home/huhu/work/CodeTransSecEval/src/security_run_evaluation.py \
        --model_name {item.model} \
        > /home/huhu/work/CodeTransSecEval/datas/function/logs/temp/securityevaluation.log 2>&1 &
    """
    return run_command(command)


@router.get("/task_status")
async def task_status(task_id: int):
    return check_process_status(task_id)
