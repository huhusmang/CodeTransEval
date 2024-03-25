import json
from extract.extract_code import extract_code


def load_json(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as file:
        datas = json.load(file)

    return datas


def dump_json(datas, json_file_path):
    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(datas, file, indent=4, ensure_ascii=False)


def dump_jsonl(datas, jsonl_file_path):
    lines = [json.dumps(x, ensure_ascii=False) for x in datas]
    with open(jsonl_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def post_process(predictions, datas):
    lang = predictions[0]["task"].split("_")[1]
    for i, prediction in enumerate(predictions):
        entry_point = datas[i]["entry_point"]
        raw_prediction = prediction["raw_prediction"]

        prediction["pro_prediction"], prediction["main_fun_name"] = extract_code(
            raw_prediction, lang, entry_point
        )
    return predictions


if __name__ == "__main__":
    projects = ["spark", "wenxin", "qwen", "minimax", "zhipu", "wenxin_3.5", "gpt4", "chatglm3", "codellama"]
    tasks = [
        "c++_java",
        "python_java",
        "c++_python",
        "java_python",
        "python_c++",
        "java_c++",
    ]

    model = projects[-1]
    datas_path = "/home/ubuntu/test_codellm/datas/datas.json"
    datas = load_json(datas_path)
    for task in tasks:
        predictions_path = (
            f"/home/ubuntu/test_codellm/result/{model}/{task}/prediction.json"
        )

        predictions = load_json(predictions_path)
        predictions = post_process(predictions, datas)
        dump_json(
            predictions,
            f"/home/ubuntu/test_codellm/result/{model}/{task}/prediction.json",
        )
        dump_jsonl(
            predictions,
            f"/home/ubuntu/test_codellm/result/{model}/{task}/prediction.jsonl",
        )
