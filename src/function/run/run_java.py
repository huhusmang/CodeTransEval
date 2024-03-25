import re
import json
import subprocess

from .gen_test_java import insert_code_str, generate_test_code, insert_testcases
from utils.util import create_json_data, load_json


def run_single_test(
    prediction, template_path, unit_tests_path, main_fun_name, datas, i
):
    """
    Runs a single test case for a Java program.

    Args:
        prediction (str): The predicted code to be inserted.
        template_path (str): The path to the template file.
        unit_tests_path (str): The path to the unit tests file.
        main_fun_name (str): The name of the main function.
        datas (list): The list of test case data.
        i (int): The index of the current test case.

    Returns:
        str: The output of the test case execution.

    Raises:
        TimeoutExpired: If the test case execution times out.
        Exception: If an error occurs during the test case execution.
    """
    insert_code_str(prediction, template_path, unit_tests_path, main_fun_name)
    input_type = datas[i - 1]["params"]["java"]["paramsType"]
    output_type = datas[i - 1]["params"]["java"]["returnType"]
    code = generate_test_code(input_type, output_type, i)
    insert_testcases(code, unit_tests_path, unit_tests_path)

    try:
        return str(
            subprocess.check_output(
                ["java", unit_tests_path], stderr=subprocess.STDOUT, timeout=60
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
        - 0: No tests passed.
        - 1: All tests passed.
        - 2: Compilation failed.
        - 3: Exception occurred during test run.(such as ArrayIndexOutOfBoundsException, etc.)
        - 4: Test failed due to not all test cases passed.(May pass partially or fail completely)
        - 5: Test timed out.

    """
    if "Timeout" in run_output:
        logger.info("Timeout!" + "\n\n")
        return 5, 0
    elif "All Passed!" in run_output:
        logger.info("Tests Passed!" + "\n\n")
        return 1, 5
    elif "compilation failed" in run_output:
        logger.info("Compilation Failed!" + "\n\n")
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


def run_java_tests(
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
    Run Java tests for the given range of tasks.

    Args:
        start (int): The starting task index.
        end (int): The ending task index.
        template_path (str): The path to the template file.
        prediction_path (str): The path to the prediction file.
        unit_test_path (str): The path to the unit test file.
        result_path (str): The path to save the results.
        datas_path (str): The path to the data file.
        prediction_num (int): The number of predictions per task.
        logger: The logger object for logging messages.

    Returns:
        list: A 2D list containing the results of each test.
    """
    results = [[0] * prediction_num for _ in range(end - start)]
    json_results = []

    datas = load_json(datas_path)
    predictions = load_json(prediction_path)
    task = predictions[0]["task"]

    for i in range(start, end):
        for j in range(prediction_num):
            task_id = f"{i}_{j}"
            index = (i - 1) * prediction_num + j
            prediction = predictions[index]["pro_prediction"]
            main_fun_name = predictions[index]["main_fun_name"]

            logger.info(f"Running task: {task_id}...")
            run_output = run_single_test(
                prediction,
                template_path,
                unit_test_path,
                main_fun_name,
                datas,
                i,
            )

            result, number = process_test_output(run_output, logger)
            results[i - start][j] = result

            data = create_json_data(task, i, j, result, number)
            json_results.append(data)

    json_results.append(create_json_data(task, "total", "total", results, 0))

    with open(result_path, "w") as file:
        json.dump(json_results, file, ensure_ascii=False, indent=4)

    return results
