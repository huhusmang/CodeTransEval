import re
from typing import List, Dict, Set


def is_special_function(function_name: str) -> bool:
    special_functions = [
        "main",
        "Main",
        "TreeNode",
        "ListNode",
        "TreeNode*",
        "ListNode*",
    ]
    return function_name in special_functions


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


def extract_function_names(lines: List[str]) -> Dict[str, int]:
    function_def_pattern = re.compile(r".*\s+\b[A-Za-z_][A-Za-z0-9_]*\b\s*\(.*\)\s*\{")
    function_names = {}
    for i, line in enumerate(lines):
        if function_def_pattern.match(line.strip()) and not is_matched_keywords(line):
            function_name = line.split("(")[0].split()[-1].strip()
            if not is_special_function(function_name):
                function_names[function_name] = i
    return function_names


def extract_main_function_name(function_names, all_function_lines):
    called_functions = set()

    # Check for function calls using a regex pattern, avoiding matches in function definitions
    for function_name, function_lines in all_function_lines.items():
        for func_name in function_names:
            # Skip recursive calls to your own functions
            if func_name == function_name:
                continue
            pattern = r"\b" + re.escape(func_name) + r"\("
            # Search for the pattern outside of function definitions
            if any(
                re.search(pattern, line)
                for line in function_lines
                if not is_matched_keywords(line)
            ):
                called_functions.add(func_name)
    main_func_name = function_names.keys() - called_functions
    return main_func_name


def extract_single_function(lines: List[str], start_line: int) -> str:
    function_lines = []
    brace_count = 0
    for line in lines[start_line:]:
        brace_count += line.count("{")
        brace_count -= line.count("}")
        function_lines.append(line)
        if brace_count == 0:
            break
    return "\n".join(function_lines)


def extract_called_functions(
    function_names: Dict[str, int],
    function: str,
    lines: List[str],
    visited: Set[str] = None,
) -> List[str]:
    if visited is None:
        visited = set()
    if function in visited:
        return []
    visited.add(function)
    extracted_functions = [extract_single_function(lines, function_names[function])]
    for name in function_names:
        if name in extracted_functions[0]:
            extracted_functions.extend(
                extract_called_functions(function_names, name, lines, visited)
            )
    return extracted_functions


def extract_relevant_cpp_functions(code: str, entry_point: str):
    lines = code.split("\n")
    # ? The nested functions of C++ are quite special, so the above regular expression cannot be searched. Naturally, there is no need for special judgments later.
    function_names = extract_function_names(lines)

    all_function_lines = {
        name: extract_single_function(lines, function_names[name]).split("\n")
        for name in function_names
    }
    extraced_main_function_name = extract_main_function_name(
        function_names, all_function_lines
    )
    main_function_name = (
        extraced_main_function_name.pop()
        if extraced_main_function_name is not None
        else entry_point
    )

    extracted_functions = extract_called_functions(
        function_names, main_function_name, lines, set()
    )
    return "\n\n".join(extracted_functions), main_function_name


if __name__ == "__main__":
    code_str = """
void func3() {
    std::cout << "test3" << std::endl;
}

void func2() {
    std::cout << "test2" << std::endl;
    func3();
}

void test_func() {
    std::cout << "test" << std::endl;
    auto func1 = []() {
        std::cout << "test1" << std::endl;
    };
    func1();
    func2();
    func3();
    testfunc();
}

    """
    main_function_name = "test_func222"
    print(extract_relevant_cpp_functions(code_str, main_function_name))
