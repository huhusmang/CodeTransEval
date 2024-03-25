import argparse
import pathlib
from models import call_llm
from utils.util import read_file, save_json_to_file


def prepare_prompt(sl_vul_code, prompt_file_path):
    prompt = read_file(prompt_file_path)
    return prompt.replace("sl_vul_code", sl_vul_code)


def save_json(problem_id, raw_prediction, sl_vul_code):
    data = {
        "problem_id": problem_id,
        "pro_prediction": "",
        "raw_prediction": raw_prediction,
        "sl_vul_code": sl_vul_code,
    }
    return data


def get_prediction(problem_dir, model_name, json_datas, json_path, prompt_file_path):
    problem_id = problem_dir.parent.name + "-" + problem_dir.name
    sl_vul_code = read_file(problem_dir / "vul.py")

    prompt = prepare_prompt(sl_vul_code, prompt_file_path)
    raw_prediction = call_llm(model_name=model_name, prompt=prompt, temperature=0.1)
    json_data = save_json(problem_id, raw_prediction, sl_vul_code)
    json_datas.append(json_data)
    save_json_to_file(json_path, json_datas)
    print(f"Task_id: {problem_id} done")


def get_predictions(dataset_path, model_name, json_path, prompt_file_path):
    json_datas = []
    for cwe_dir in sorted(dataset_path.iterdir()):
        for problem_dir in sorted(cwe_dir.iterdir()):
            if (problem_dir / "vul.py").exists():
                get_prediction(problem_dir, model_name, json_datas, json_path, prompt_file_path)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name", type=str, default="gpt4", help="Name of the model"
    )
    parser.add_argument(
        "--predicitons_base_path",
        type=str,
        default="/home/ubuntu/CodeTransSecEval/data/predictions",
        help="Base path to the result JSON file",
    )
    parser.add_argument(
        "--datasets_path",
        type=str,
        default="/home/ubuntu/CodeTransSecEval/data/datasets",
        help="Datasets path",
    )
    parser.add_argument(
        "--prompt_file_path",
        type=str,
        default="/home/ubuntu/CodeTransSecEval/src/prompt.txt",
        help="Prompt file path",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    predicitons_base_path = pathlib.Path(args.predicitons_base_path)
    dataset_path = pathlib.Path(args.datasets_path)
    json_path = predicitons_base_path / (args.model_name + ".json")
    prompt_file_path = pathlib.Path(args.prompt_file_path)
    model_name = args.model_name

    get_predictions(dataset_path, model_name, json_path, prompt_file_path)


if __name__ == "__main__":
    main()
