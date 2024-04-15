import json
import argparse
import pathlib
from typing import List, Dict

from models import call_llm
from function.extract.extract_code import extract_code


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    return content


def load_json(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as file:
        datas = json.load(file)

    return datas


def save_json(
    task,
    problem_id,
    prediciton_id,
    pro_prediction,
    main_fun_name,
    raw_prediction,
    sl_gold_code,
    tl_gold_code,
):
    data = {
        "task": task,
        "problem_id": problem_id,
        "prediction_id": prediciton_id,
        "pro_prediction": pro_prediction,
        "main_fun_name": main_fun_name,
        "raw_prediction": raw_prediction,
        "sl_gold_code": sl_gold_code,
        "tl_gold_code": tl_gold_code,
    }

    return data


def prepare_prompt(prompt_file_path, sl, tl, sc, params):
    with open(prompt_file_path, encoding="utf-8") as f:
        prompt = f.read().strip()

    prompt = (
        prompt.replace("SL", sl)
        .replace("TL", tl)
        .replace("SC", sc)
        .replace("PARAMS", params)
    )

    return prompt


def save_results(file_path: str, data: List[Dict], jsonl: bool = False):
    with open(file_path, "w", encoding="utf-8") as file:
        if jsonl:
            lines = [json.dumps(x, ensure_ascii=False) for x in data]
            file.write("\n".join(lines))
        else:
            json.dump(data, file, ensure_ascii=False, indent=4)


def main(
    model_name,
    task,
    start,
    end,
    prediction_nums,
    prompt_file_path,
    answer_base_path,
    datas_path,
    json_path,
    jsonl_path,
    is_save,
):
    sl, tl = task.split("_")
    datas = load_json(datas_path)

    json_datas = []
    for i in range(start, end):
        sl_gold_code = read_file(pathlib.Path(answer_base_path) / str(i) / f"{sl}")
        tl_gold_code = read_file(pathlib.Path(answer_base_path) / str(i) / f"{tl}")
        params = str(datas[i - 1]["params"][tl])
        prompt = prepare_prompt(prompt_file_path, sl, tl, sl_gold_code, params)

        for j in range(prediction_nums):
            raw_prediction = call_llm(
                model_name=model_name, prompt=prompt, temperature=0.1
            ).response
            prediction, main_fun_name = extract_code(
                raw_prediction,
                tl,
                datas[i - 1]["entry_point"],
            )
            result = prediction if prediction != "" else raw_prediction

            json_data = save_json(
                task,
                i,
                j,
                result,
                main_fun_name,
                raw_prediction,
                sl_gold_code,
                tl_gold_code,
            )
            json_datas.append(json_data)

            print("Task_id: " + str(i) + "_" + str(j) + "    done")

    if is_save:
        save_results(json_path, json_datas)
        save_results(jsonl_path, json_datas, jsonl=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name", type=str, default="gpt-4-0125-preview", help="Name of the model"
    )
    parser.add_argument("--task", default="java_python", help="Task name")
    parser.add_argument(
        "--start", type=int, default=1, help="Start index of the test tasks"
    )
    parser.add_argument(
        "--end", type=int, default=2, help="End index of the test tasks"
    )
    parser.add_argument(
        "--prediction_nums",
        type=int,
        default=1,
        help="Number of predictions to be generated for each question",
    )
    parser.add_argument(
        "--predictions_base_path",
        default="/home/huhu/work/CodeTransSecEval/datas/function/predictions",
        help="Path to the answer file",
    )
    parser.add_argument(
        "--answer_base_path",
        type=str,
        default="/home/huhu/work/CodeTransSecEval/datas/function/gold_answer",
        help="Base path for gold answers",
    )
    parser.add_argument(
        "--datas_path",
        type=str,
        default="/home/huhu/work/CodeTransSecEval/datas/function/datas.json",
        help="datas_json path",
    )
    parser.add_argument(
        "--prompt_file_path",
        type=str,
        default="/home/huhu/work/CodeTransSecEval/src/prompts/function_prompt.txt",
    )
    parser.add_argument(
        "--is_save",
        action='store_true',
        help="Whether to save the results to file",
    )
    args = parser.parse_args()

    json_path = (
        pathlib.Path(args.predictions_base_path)
        / args.model_name
        / args.task
        / "prediction.json"
    )
    jsonl_path = (
        pathlib.Path(args.predictions_base_path)
        / args.model_name
        / args.task
        / "prediction.jsonl"
    )
    if not json_path.parent.exists():
        json_path.parent.mkdir(parents=True, exist_ok=True)

    main(
        model_name=args.model_name,
        task=args.task,
        start=args.start,
        end=args.end,
        prediction_nums=args.prediction_nums,
        answer_base_path=args.answer_base_path,
        datas_path=args.datas_path,
        prompt_file_path=args.prompt_file_path,
        json_path=json_path,
        jsonl_path=jsonl_path,
        is_save=args.is_save,
    )
