import re
from typing import List, Dict, Set


# Because even if the judgment of function_def_pattern is passed, some loop statements such as `if` `while` etc. will still be matched.
# In view of the fact that java functions generally have keywords such as public static, here is how to determine whether it is a function definition statement through keywords such as public static.
# C++ also has this problem, but C++ generally does not have keywords such as public static, so it is used to judge all loops and branch statements such as if while
#In fact, java can combine the two judgment methods~
def is_matched_keywords(line: str) -> bool:
    if (
        (
            line.strip().startswith("public static")
            or line.strip().startswith("public ")
            or line.strip().startswith("private static")
            or line.strip().startswith("private ")
        )
        and "(" in line
        and ")" in line
        and "{" in line
    ):
        return True


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


def extract_function_names(lines: List[str]) -> Dict[str, int]:
    function_def_pattern = re.compile(r".*\s+\b[A-Za-z_][A-Za-z0-9_]*\b\s*\(.*\)\s*\{")
    function_names = {}
    for i, line in enumerate(lines):
        if function_def_pattern.match(line.strip()) and is_matched_keywords(line):
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


def add_public_static(function_lines):
    """
    The domains of output for some models are different. Some are public static, some are private static,
    some are static, some are public, and some are private. So standardize each extracted function here.
    """
    declare_line = function_lines[0]
    declare_line = (
        declare_line.replace("public", "")
        .replace("static", "")
        .replace("private", "")
        .replace("protected", "")
        .strip()
    )
    function_lines[0] = "public static " + declare_line


def extract_single_function(lines: List[str], start_line: int) -> str:
    function_lines = []
    brace_count = 0
    for line in lines[start_line:]:
        brace_count += line.count("{")
        brace_count -= line.count("}")
        function_lines.append(line)
        if brace_count == 0:
            break
    add_public_static(function_lines)
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


def extract_relevant_java_functions(code, entry_point):
    """
    Extracts the main function and any functions it calls from the Java class code.
    """
    # Split the code into lines
    lines = code.split("\n")
    # ? Java does not have built-in functions, so no special judgment is needed later.
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
public class Main {
    public static void testFunc() {
        System.out.println("test");
        func1();
        func2();
        testFunc();
    }

    public static void func1() {
        System.out.println("test1");
    }

    public static void func2() {
        System.out.println("test2");
        func3();
    }

    public static void func3() {
        System.out.println("test3");
    }
}
    """
    main_function_name = "testFunc1"
    print(extract_relevant_java_functions(code_str, main_function_name))
