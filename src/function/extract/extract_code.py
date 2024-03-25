import re
from .extract_code_python import extract_relevant_python_functions
from .extract_code_java import extract_relevant_java_functions
from .extract_code_cpp import extract_relevant_cpp_functions


def replace_escape_characters(code_str):
    return code_str.replace("\\n", "\n").replace('\\"', '"')


def find_code_pattern(code_str, language):
    pattern = r"```" + language + r"\n(.*?)\n```"
    matches = re.findall(pattern, code_str, re.DOTALL)
    # Because some models use "c++" instead of "cpp"(little foolish), so we need to add a judgment here.
    if not matches and language == "cpp":
        pattern = r"```c\+\+\n(.*?)\n```"
        matches = re.findall(pattern, code_str, re.DOTALL)
    # Some models does not use the language name as the code block name, so we need to add a judgment here.
    if not matches:
        pattern = r"```\n(.*?)\n```"
        matches = re.findall(pattern, code_str, re.DOTALL)
    return matches


def extract_relevant_functions(code, main_function_name, language):
    """
    Extracts the main function and any functions it calls from the code.
    """
    if language == "python":
        return extract_relevant_python_functions(code, main_function_name)
    elif language == "java":
        return extract_relevant_java_functions(code, main_function_name)
    elif language == "cpp":
        return extract_relevant_cpp_functions(code, main_function_name)
    else:
        return code


def extract_code(code_str, language, entry_point):
    if language == "c++":
        language = "cpp"

    code_str = replace_escape_characters(code_str)
    matches = find_code_pattern(code_str, language)
    # TODO: There may be some inaccuracies here, as only the first matching code block is taken as the block to be extracted.
    pro_code = matches[0] if matches else code_str

    try:
        result, main_function_name = extract_relevant_functions(pro_code, entry_point, language)
    except Exception as e:
        result = pro_code

    return result, main_function_name


if __name__ == "__main__":
    """
    Response really returns `true_returned_str`, but print returns `print_returned_str`, because print escapes the string, and the string written into the file is also the escaped string. 
    However, when the string written into the file is read out, the escape character is automatically converted to the original character, that is, `true_returned_str`.
    """
    print_returned_str = " [java]:\n\n```java\npublic int testfunc(int[] nums, int k) {\n    int ans = 0;\n    for (int i = 0; i < 31; i++) {\n        int cnt1 = 0;\n        for (int x : nums) {\n            cnt1 += x >> i & 1;\n        }\n        if (cnt1 >= k) {\n            ans |= 1 << i;\n        }\n    }\n    return ans;\n}\n```"
    true_returned_str = '" [java]:\\n\\n```java\\nint testfunc(int[] nums, int k) {\\n    int ans = 0;\\n    for (int i = 0; i < 31; i++) {\\n        int cnt1 = 0;\\n        for (int x : nums) {\\n            cnt1 += x >> i & 1;\\n        }\\n        if (cnt1 >= k) {\\n            ans |= 1 << i;\\n        }\\n    }\\n    return ans;\\n}\\n```"'

    extracted_code_blocks_1 = extract_code(print_returned_str, pattern=1)
    extracted_code_blocks_2 = extract_code(true_returned_str)
    extracted_code_blocks_3 = extract_code(eval(true_returned_str), pattern=1)

    print(extracted_code_blocks_2)
