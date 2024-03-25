import json


base_path = "/home/huhu/work/CodeTransSecEval/datas/function/predictions/"
models = ["spark", "wenxin", "qwen", "minimax", "zhipu", "wenxin_3.5", "gpt4", "chatglm3", "codellama"]
tasks = ["c++_java", "python_c++", "c++_python", "java_python", "python_java", "java_c++"]

json_datas = []
for model in models:
    json_data = {
        "model": model,
        "tasks_results": []
    }
    for task in tasks:
        json_path = base_path + model + "/" + task + "/results.json"
        with open(json_path, "r") as f:
            datas = json.load(f)
        result = datas[-1]["results"]

        json_data["tasks_results"].append({
            "task": task,
            "result": result
        })

    json_datas.append(json_data)

with open(base_path + "results.json", "w") as f:
    json.dump(json_datas, f, indent=4)