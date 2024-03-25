import json
import re


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def load_json(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json_to_file(json_path, json_datas):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_datas, f, ensure_ascii=False, indent=4)


def replace_func_name(code_str, entry_point):
    if code_str.find(entry_point) != -1:
        return code_str.replace(entry_point, "testfunc")
    else:
        return code_str


def create_json_data(task, problem_id, prediction_id, answer_type, number):
    return {
        "task": task,
        "problem_id": problem_id,
        "prediction_id": prediction_id,
        "answer_type": answer_type,
        "Passed_testcase_nums": number,
    }


def camel_to_snake(name):
    """
    Convert a camelCase string to snake_case.
    """
    snake = [name[0].lower()]
    for char in name[1:]:
        if char.isupper():
            snake.append("_")
            snake.append(char.lower())
        else:
            snake.append(char)
    return "".join(snake)


def is_matched_keywords(line):
    stripped_line = line.strip()
    if (
        (
            ("else" in line)
            and ((stripped_line.startswith("else")) or (stripped_line.startswith("}")))
        )
        or (("if" in line) and (stripped_line.startswith("if")))
        or (("for" in line) and (stripped_line.startswith("for")))
        or (("while" in line) and (stripped_line.startswith("while")))
        or (("switch" in line) and (stripped_line.startswith("switch")))
        or (
            ("case" in line)
            and ((stripped_line.startswith("case")) or (stripped_line.startswith("}")))
        )
        or (("do" in line) and (stripped_line.startswith("do")))
        or (("try" in line) and (stripped_line.startswith("try")))
        or (
            ("catch" in line)
            and ((stripped_line.startswith("catch")) or (stripped_line.startswith("}")))
        )
    ):
        return True
    else:
        return False


def extract_main_func(lines):
    function_def_pattern = re.compile(r".*\s+\b[A-Za-z_][A-Za-z0-9_]*\b\s*\(.*\)\s*\{")
    line_num = -1
    for i, line in enumerate(lines):
        if function_def_pattern.match(line.strip()) and not is_matched_keywords(line):
            if "main" in line:
                line_num = i
                break

    def extract_single_function(start_line):
        function_lines = []
        brace_count = 0
        for line in lines[start_line:]:
            if "{" in line:
                brace_count += line.count("{")
            if "}" in line:
                brace_count -= line.count("}")
            function_lines.append(line)
            if brace_count == 0:
                break
        return "\n".join(function_lines)

    if line_num != -1:
        return extract_single_function(line_num)
    else:
        return ""
