import json
from metrics import estimate_pass_at_k, estimate_codebleu


def load_json(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        results = json.load(file)

    return results


def pre_process(results, prediction_num):
    num_samples = prediction_num
    num_correct = [0] * len(results)

    for i in range(len(results)):
        for j in range(num_samples):
            if results[i][j] == 1:
                num_correct[i] += 1

    return num_samples, num_correct


def eval_pass_at_k(results_json_path, k, prediction_num):
    pre_results = load_json(results_json_path)

    results = pre_results[-1]["answer_type"]
    num_samples, num_correct = pre_process(results, prediction_num)

    pass_at_k = estimate_pass_at_k(num_samples, num_correct, k)

    return pass_at_k


def eval_codebleu(prediction_json_path):
    prediction_datas = load_json(prediction_json_path)

    lang = prediction_datas[0]["task"].split("_")[1]
    if lang == "c++":
        lang = "cpp"
    references = []
    predictions = []

    for prediction_data in prediction_datas:
        references.append(prediction_data["tl_gold_code"])
        predictions.append(prediction_data["pro_prediction"])

    codebleu = estimate_codebleu(references, predictions, lang)
    return codebleu


def eval_run_metric(results_json_path, prediction_num):
    pre_results = load_json(results_json_path)
    results = pre_results[-1]["answer_type"]

    answer_type_nums = {
        "all_passed": 0,
        "compilation_failed": 0,
        "runtime_error": 0,
        "wrong_answer": 0,
        "timeout_error": 0,
        "other_error": 0  # C++: segmentation fault, python: memory error
    }

    for i in range(len(results)):
        for j in range(prediction_num):
            if results[i][j] == 1:
                answer_type_nums["all_passed"] += 1
            elif results[i][j] == 2:
                answer_type_nums["compilation_failed"] += 1
            elif results[i][j] == 3:
                answer_type_nums["runtime_error"] += 1
            elif results[i][j] == 4:
                answer_type_nums["wrong_answer"] += 1
            elif results[i][j] == 5:
                answer_type_nums["timeout_error"] += 1
            elif results[i][j] == 0:
                answer_type_nums["other_error"] += 1

    return answer_type_nums


def eval_average_passed_testcases_num(results_json_path):
    pre_results = load_json(results_json_path)

    passed_testcase_nums_list = []
    for i in range(len(pre_results) - 1):
        result = pre_results[i]
        passed_testcase_nums_list.append(int(result["Passed_testcase_nums"]))

    passed_testcase_nums = sum(passed_testcase_nums_list)
    average_passed_testcase_rates = passed_testcase_nums / 500

    return passed_testcase_nums_list, average_passed_testcase_rates


def save_results(
    pass_at_k,
    k,
    passed_testcase_nums_list,
    average_passed_testcase_rates,
    codebleu,
    answer_type_nums,
    results_json_path,
):
    results = {
        f"Pass@{k} estimates for each problem": str(pass_at_k),
        "Passed questions": sum(pass_at_k),
        "Total questions": len(pass_at_k),
        f"Pass@{k} rate": (sum(pass_at_k)) / (len(pass_at_k)),
        "Passed_testcase_nums_list": str(passed_testcase_nums_list),
        "Average_passed_testcase_rates": average_passed_testcase_rates,
        "CodeBLEU": codebleu,
        "Answer_type_nums": answer_type_nums,
    }

    results_json = load_json(results_json_path)
    results_json[-1]["results"] = results

    with open(results_json_path, "w", encoding="utf-8") as file:
        json.dump(results_json, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    models = [
        "spark",
        "wenxin",
        "qwen",
        "minimax",
        "zhipu",
        "wenxin_3.5",
        "gpt4",
        "chatglm3",
        "codellama",
    ]
    tasks = [
        "c++_java",
        "python_c++",
        "c++_python",
        "java_python",
        "python_java",
        "java_c++",
    ]

    # model = models[0]
    # task = tasks[-1]

    for model in models:
        for task in tasks:
            results_json_path = (
                f"/home/huhu/work/CodeTransSecEval/datas/function/predictions/{model}/{task}/results.json"
            )
            k = 1
            prediction_num = 1

            pass_at_k = eval_pass_at_k(results_json_path, k, prediction_num)
            # convert ndarray to list
            pass_at_k = pass_at_k.tolist()
            print(f"Pass@{k} estimates for each problem = {pass_at_k}")
            print(f"Passed questions = {sum(pass_at_k)}")
            print(f"Total questions = {len(pass_at_k)}")
            print(f"Pass@{k} rate = {(sum(pass_at_k)) / (len(pass_at_k))}")

            (
                passed_testcase_nums_list,
                average_passed_testcase_rates,
            ) = eval_average_passed_testcases_num(results_json_path)
            print(f"passed_testcase_nums_list = {passed_testcase_nums_list}")
            print(f"average_passed_testcase_rates = {average_passed_testcase_rates}")

            prediction_json_path = (
                f"/home/huhu/work/CodeTransSecEval/datas/function/predictions/{model}/{task}/prediction.json"
            )
            codebleu = eval_codebleu(prediction_json_path)
            print(f"CodeBLEU = {codebleu}")

            answer_type_nums = eval_run_metric(results_json_path, prediction_num)
            print(f"answer_type_nums = {answer_type_nums}\n\n")

            save_results(
                pass_at_k,
                k,
                passed_testcase_nums_list,
                average_passed_testcase_rates,
                codebleu,
                answer_type_nums,
                results_json_path,
            )
