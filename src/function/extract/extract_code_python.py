import re
from typing import List, Dict, Set


def adjust_indentation(code_str):
    lines = code_str.split("\n")
    base_indentation = find_base_indentation(lines)
    adjusted_lines = remove_base_indentation(lines, base_indentation)
    return "\n".join(adjusted_lines)


def find_base_indentation(lines):
    for line in lines:
        stripped_line = line.lstrip()
        if stripped_line:
            return len(line) - len(stripped_line)


def remove_base_indentation(lines, base_indentation):
    return [
        line[base_indentation:] if len(line) > base_indentation else line
        for line in lines
    ]


def extract_function_names(lines):
    function_names = {}
    for i, line in enumerate(lines):
        if line.strip().startswith("def "):
            function_name = line.split("(")[0].replace("def ", "").strip()
            if function_name not in ["__init__", "main", "TreeNode", "ListNode"]:
                function_names[function_name] = i
    return function_names


# ? 这里假设主函数没有被其他函数调用，或者只被 main 函数以及直接调用，这两个已经在提取函数名和提取all_function_lines时被屏蔽了
# ? 同时假设没有第二个不被调用的函数，这种情况应该很少~
def extract_main_function_name(function_names, all_function_lines):
    called_functions = set()

    # TODO: 更好的实现方法是每个提取出的函数体检查内部的调用函数然后 - 本函数的 name，即 called_function = called_functions - function_names
    # TODO：那所有的 called_functions 就是相加，
    # Check for function calls using a regex pattern, avoiding matches in function definitions
    for function_name, function_lines in all_function_lines.items():
        for func_name in function_names:
            # 跳过递归调用自己的函数
            if func_name == function_name:
                continue
            pattern = r"\b" + re.escape(func_name) + r"\("
            # Search for the pattern outside of function definitions
            if any(
                re.search(pattern, line)
                for line in function_lines
                if not line.strip().startswith("def")
            ):
                called_functions.add(func_name)
    main_func_name = function_names.keys() - called_functions
    return main_func_name


def extract_single_function(lines, start_line):
    function_lines = []
    indent_level = None
    for line_num, line in enumerate(lines[start_line:]):
        stripped_line = line.strip()
        if stripped_line:
            # counts the leading spaces or tabs, setting the indent_level for the first non-empty line of the function.
            if indent_level is None:
                indent_level = len(line) - len(stripped_line)
            # TODO: Maybe there has some Potential Logical Flaws
            # Check for Function End: determine if the current line marks the end of the function being extracted.
            # if (
            #     not stripped_line.startswith("def ")
            #     and len(line) - len(stripped_line) == indent_level
            # ) or (
            #     stripped_line.startswith("def ")
            #     and len(line) - len(stripped_line) == indent_level
            #     and line_num != 0
            # ):
            #     break
            if (len(line) - len(stripped_line) == indent_level) and (line_num != 0):
                break
        function_lines.append(line)
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
        # avoiding extracting the nested function
        if (name in extracted_functions[0]) and (
            re.findall(r"def\s+" + name + r"\s*\(", extracted_functions[0]) == []
        ):
            extracted_functions.extend(
                extract_called_functions(function_names, name, lines, visited)
            )
    return extracted_functions


def extract_relevant_python_functions(code, entry_point):
    """
    Extracts the main function and any functions it calls from the Python code.
    """
    lines = code.split("\n")
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

    # 没有直接用上面的 all_function_lines 进行转化是防止嵌套函数的重复提取
    extracted_functions = extract_called_functions(
        function_names, main_function_name, lines, set()
    )

    code_str = "\n\n".join(extracted_functions)
    # delete self
    code_str = code_str.replace("self,", "").replace("self.", "")
    return adjust_indentation(code_str), main_function_name


if __name__ == "__main__":
    code_str = """
    def test_func():
        print("test")
        def func1():
            print("test1")
        test_func()
        func1()
        func2()
        func3()
    def func2():
        print("test2")
        func2()
        func3()
    def func3():
        print("test3")
    def func4():
        print("test4")

    test_func()
    """
    main_function_name = "test_func1"
    print(extract_relevant_python_functions(code_str, main_function_name))
