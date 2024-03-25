import re
import json
import pathlib
import subprocess

from .gen_test_cpp import insert_code_str, generate_test_code, insert_testcases
from utils.util import create_json_data, load_json


def compile_code(unit_tests_path, unit_tests_dir):
    try:
        subprocess.check_output(
            [
                "g++",
                "-O0",
                "-std=c++20",
                unit_tests_path,
                "-o",
                f"{unit_tests_dir}/out.o",
            ],
            stderr=subprocess.STDOUT,
            timeout=60,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def run_code(unit_tests_dir):
    try:
        if pathlib.Path(f"{unit_tests_dir}/out.o").exists():
            return str(subprocess.check_output([f"{unit_tests_dir}/out.o"], timeout=60))
    except subprocess.TimeoutExpired:
        return "Timeout"
    except Exception as e:
        return e.output.decode("utf-8")


def process_run_output(run_output, logger):
    """
    Process the output of a run and return a tuple representing the result.

    Args:
        run_output (str): The output of the run.

    Returns:
        tuple: A tuple representing the result of the run. The first element of the tuple
        indicates the status code, and the second element indicates the number of tests passed.

    Status Codes:
        - 0: No result
        - 1: All tests passed
        - 2: Compilation failed.
        - 3: Exception occurred during test run.(such as ArrayIndexOutOfBoundsException, etc.)
        - 4: Test failed due to not all test cases passed.(May pass partially or fail completely)
        - 5: Timeout

    """
    if "Timeout" in run_output:
        logger.info("Timeout!" + "\n\n")
        return 5, 0
    elif "All Passed!" in run_output:
        logger.info("Tests Passed!" + "\n\n")
        return 1, 5
    elif "An exception occurred" in run_output or "Test Failed!" in run_output:
        logger.info(f"run_output: {run_output}" + "\n\n")
        match = re.search(r"Passed (\d+)/", run_output)
        return 3 if "Exception" in run_output else 4, int(
            match.group(1)
        ) if match else 0
    else:
        return 0, 0


def run_single_test(
    prediction, template_path, unit_tests_path, main_fun_name, datas, i
):
    """
    Runs a single test case for a C++ program.

    Args:
        prediction (str): The C++ code to be tested.
        template_path (str): The path to the template file.
        unit_tests_path (str): The path to the unit tests file.
        main_fun_name (str): The name of the main function in the C++ code.
        datas (list): The list of test case data.
        i (int): The index of the current test case.

    Returns:
        str: The output of running the test case.

    Raises:
        CompilationError: If the code fails to compile.
    """
    insert_code_str(prediction, template_path, unit_tests_path, main_fun_name)
    input_type = datas[i - 1]["params"]["c++"]["paramsType"]
    output_type = datas[i - 1]["params"]["c++"]["returnType"]
    code = generate_test_code(input_type, output_type, i)
    insert_testcases(code, unit_tests_path, unit_tests_path)

    unit_tests_dir = pathlib.Path(unit_tests_path).parent

    if not compile_code(unit_tests_path, unit_tests_dir):
        return "Compilation Failed!"
    else:
        run_output = run_code(unit_tests_dir)
        return run_output


def run_cpp_tests(
    start,
    end,
    template_path,
    prediction_path,
    unit_test_path,
    result_path,
    datas_path,
    prediction_num,
    logger,
):
    """
    Run C++ tests for a given range of tasks.

    Args:
        start (int): The starting task index.
        end (int): The ending task index.
        template_path (str): The path to the C++ template file.
        prediction_path (str): The path to the prediction file.
        unit_test_path (str): The path to the unit test file.
        result_path (str): The path to save the result file.
        datas_path (str): The path to the datas file.
        prediction_num (int): The number of predictions per task.
        logger (Logger): The logger object for logging.

    Returns:
        list: A 2D list containing the results of the tests.

    """
    results = [[0] * prediction_num for _ in range(end - start)]
    json_results = []

    datas = load_json(datas_path)
    predictions = load_json(prediction_path)
    task = predictions[0]["task"]

    for i in range(start, end):
        for j in range(prediction_num):
            task_id = str(i) + "_" + str(j)
            index = (i - 1) * prediction_num + j
            prediction = predictions[index]["pro_prediction"]
            main_fun_name = predictions[index]["main_fun_name"]

            logger.info(f"Running task: {task_id}...")
            run_output = run_single_test(
                prediction, template_path, unit_test_path, main_fun_name, datas, i
            )
            if run_output == "Compilation Failed!":
                results[i - start][j] = 2
                number = 0
                logger.info("Compilation Failed!" + "\n\n")
            else:
                result, number = process_run_output(run_output, logger)
                results[i - start][j] = result

            data = create_json_data(task, i, j, results[i - start][j], number)
            json_results.append(data)

    json_results.append(create_json_data(task, "total", "total", results, 0))

    with open(result_path, "w") as file:
        json.dump(json_results, file, ensure_ascii=False, indent=4)

    return results
