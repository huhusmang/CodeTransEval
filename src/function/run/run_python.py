import re
import json
import subprocess

from .gen_test_python import insert_test_code, insert_code_str
from utils.util import create_json_data, load_json


def run_single_test(prediction, template_path, unit_tests_path, main_fun_name, i):
    """
    Runs a single test case.

    Args:
        prediction (str): The prediction code to be inserted.
        template_path (str): The path to the template file.
        unit_tests_path (str): The path to the unit tests file.
        main_fun_name (str): The name of the main function.
        i (int): The index of the test case.

    Returns:
        str: The output of the test case execution.
    """
    insert_code_str(prediction, template_path, unit_tests_path, main_fun_name)
    insert_test_code(unit_tests_path, unit_tests_path, i)

    try:
        return str(
            subprocess.check_output(
                ["python3", unit_tests_path], stderr=subprocess.STDOUT, timeout=60
            )
        )
    except subprocess.TimeoutExpired:
        return "Timeout"
    except Exception as e:
        return e.output.decode("utf-8")


def process_test_output(run_output, logger):
    """
    Process the output of a test run and return a tuple representing the result.

    Args:
        run_output (str): The output of the test run.

    Returns:
        tuple: A tuple representing the result of the test run. The first element
        indicates the status code, and the second element indicates the number of
        tests passed.

    Status Codes:
        - 0: No relevant information found in the output.
        - 1: All tests passed.
        - 2: SyntaxError encountered.
        - 3: Exception encountered.(such as ValueError, TypeError, etc.)
        - 4: Test failed due to not all test cases passed.(May pass partially or fail completely)
        - 5: Timeout occurred.

    Note:
        The function looks for specific patterns in the `run_output` to determine
        the status code and the number of tests passed. If no relevant information
        is found, the function returns (0, 0).
    """
    if "Timeout" in run_output:
        logger.info("Timeout!" + "\n\n")
        return 5, 0
    elif "All Passed!" in run_output:
        logger.info("Tests Passed!" + "\n\n")
        return 1, 5
    elif "SyntaxError" in run_output:
        logger.info("SyntaxError!" + "\n\n")
        logger.info(f"run_output: {run_output}" + "\n\n")
        return 2, 0
    elif "Exception" in run_output or "Test Failed!" in run_output:
        logger.info(f"run_output: {run_output}" + "\n\n")
        match = re.search(r"Passed (\d+)/", run_output)
        return 3 if "Exception" in run_output else 4, int(
            match.group(1)
        ) if match else 0
    else:
        return 0, 0


def run_python_tests(
    start,
    end,
    template_path,
    prediction_path,
    unit_test_path,
    result_path,
    prediction_num,
    logger,
):
    """
    Run Python tests for a given range of tasks.

    Args:
        start (int): The starting task index.
        end (int): The ending task index.
        template_path (str): The path to the template file.
        prediction_path (str): The path to the prediction file.
        unit_test_path (str): The path to the unit test file.
        result_path (str): The path to save the result file.
        prediction_num (int): The number of predictions per task.
        logger: The logger object for logging messages.

    Returns:
        list: A 2D list of test results for each task and prediction.

    """
    results = [[0] * prediction_num for _ in range(end - start)]
    json_results = []

    predictions = load_json(prediction_path)
    task = predictions[0]["task"]

    for i in range(start, end):
        for j in range(prediction_num):
            task_id = f"{i}_{j}"
            index = (i - 1) * prediction_num + j
            answer = predictions[index]["pro_prediction"]
            main_fun_name = predictions[index]["main_fun_name"]

            logger.info(f"Running task: {task_id}...")
            run_output = run_single_test(
                answer, template_path, unit_test_path, main_fun_name, i
            )

            result, number = process_test_output(run_output, logger)
            results[i - start][j] = result

            data = create_json_data(task, i, j, result, number)
            json_results.append(data)

    json_results.append(create_json_data(task, "total", "total", results, 0))

    with open(result_path, "w") as file:
        json.dump(json_results, file, ensure_ascii=False, indent=4)

    return results
