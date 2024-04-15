import argparse
import logging
from pathlib import Path
from datetime import datetime

from function.run.run_cpp import run_cpp_tests
from function.run.run_java import run_java_tests
from function.run.run_python import run_python_tests


def init_base_data_path(base_data_path):
    paths = [
        "/home/huhu/work/CodeTransSecEval/src/templates/template.py",
        "/home/huhu/work/CodeTransSecEval/src/utils/gen_test_java.py",
        "/home/huhu/work/CodeTransSecEval/src/utils/gen_test_cpp.py",
    ]

    for path in paths:
        with open(path, "r") as file:
            content = file.read()
            content = content.replace("{base_data_path}", base_data_path)

        with open(path, "w") as file:
            file.write(content)


def setup_logger(log_path):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=log_path,
    )
    return logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="wenxin_3.5", help="Model name")
    parser.add_argument("--task", default="c++_python", help="Task name")
    parser.add_argument("--start", default=93, type=int, help="Start index for test")
    parser.add_argument("--end", default=94, type=int, help="End index for test")
    parser.add_argument(
        "--data_base_path",
        default="/home/huhu/work/CodeTransSecEval/datas/function",
        help="Path to the data file",
    )
    parser.add_argument(
        "--template_base_path",
        default="/home/huhu/work/CodeTransSecEval/src/templates",
        help="Path to the template file",
    )
    parser.add_argument(
        "--predictions_base_path",
        default="/home/huhu/work/CodeTransSecEval/datas/function/predictions",
        help="Path to the answer file",
    )
    parser.add_argument(
        "--unit_test_base_path",
        default="/home/huhu/work/CodeTransSecEval/datas/function/unit_tests",
        help="Path to the unit tests file",
    )
    parser.add_argument(
        "--results_base_path",
        default="/home/huhu/work/CodeTransSecEval/datas/function/predictions",
        help="Path to the results file",
    )
    parser.add_argument(
        "--datas_path",
        default="/home/huhu/work/CodeTransSecEval/datas/function/datas.json",
        help="Path to the json file",
    )
    parser.add_argument(
        "--log_base_path",
        default="/home/huhu/work/CodeTransSecEval/datas/function/logs",
        help="Path to the log file",
    )
    parser.add_argument(
        "--prediction_numss", default=1, type=int, help="Number of predictions"
    )

    return parser.parse_args()


def get_suffix(target_language):
    if target_language == "c++":
        return "cpp"
    if target_language == "python":
        return "py"
    return target_language


def get_template_path(base_path, suffix):
    return Path(base_path) / f"template.{suffix}"


def get_prediction_path(base_path, model, task):
    return Path(base_path) / model / task / "prediction.json"


def get_unit_test_path(base_path, model, task, suffix):
    return Path(base_path) / model / task / f"test.{suffix}"


def get_result_path(base_path, model, task):
    return Path(base_path) / model / task / "results.json"


def get_log_path(base_path, model, task):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = Path(base_path) / model / task / f"{current_time}.log"
    if not log_path.parent.exists():
        log_path.parent.mkdir(parents=True, exist_ok=True)
    return log_path


def run_tests(
    target_language,
    args,
    template_path,
    prediction_path,
    unit_test_path,
    result_path,
    logger,
):
    if target_language == "python":
        return run_python_tests(
            start=args.start,
            end=args.end,
            template_path=template_path,
            prediction_path=prediction_path,
            unit_test_path=unit_test_path,
            result_path=result_path,
            prediction_nums=args.prediction_nums,
            logger=logger,
        )
    elif target_language == "java":
        return run_java_tests(
            start=args.start,
            end=args.end,
            template_path=template_path,
            prediction_path=prediction_path,
            unit_test_path=unit_test_path,
            result_path=result_path,
            datas_path=args.datas_path,
            prediction_nums=args.prediction_nums,
            logger=logger,
        )
    elif target_language == "c++":
        return run_cpp_tests(
            start=args.start,
            end=args.end,
            template_path=template_path,
            prediction_path=prediction_path,
            unit_test_path=unit_test_path,
            result_path=result_path,
            datas_path=args.datas_path,
            prediction_nums=args.prediction_nums,
            logger=logger,
        )
    else:
        raise ValueError(f"Invalid target language: {target_language}")


def main(init: bool = False):
    args = parse_arguments()

    if init:
        init_base_data_path(args.data_base_path)

    target_language = args.task.split("_")[1]
    suffix = get_suffix(target_language)

    template_path = get_template_path(args.template_base_path, suffix)
    prediction_path = get_prediction_path(
        args.predictions_base_path, args.model, args.task
    )
    unit_test_path = get_unit_test_path(
        args.unit_test_base_path, args.model, args.task, suffix
    )
    result_path = get_result_path(args.results_base_path, args.model, args.task)
    log_path = get_log_path(args.log_base_path, args.model, args.task)

    logger = setup_logger(log_path)

    results = run_tests(
        target_language,
        args,
        template_path,
        prediction_path,
        unit_test_path,
        result_path,
        logger,
    )

    logger.info(f"results: {results}")


if __name__ == "__main__":
    main(init=False)
