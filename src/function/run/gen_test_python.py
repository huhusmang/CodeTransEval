import os
from utils.util  import replace_func_name


def insert_code(python_file_path, template_file_path, modified_file_path, question_name):
    # Function to read the content of a file
    def read_file(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            return file.read()

    # Reading the contents of both files
    python_content = read_file(python_file_path)
    # replace funcname
    python_content = replace_func_name(python_content, question_name)

    template_content = read_file(template_file_path)

    # Finding the position of the comments in the template file
    insertion_start = template_content.find("# Write the target function here")
    insertion_end = template_content.find("# End here", insertion_start)

    # Splitting the template content into two parts: before and after the insertion point
    before_insertion = template_content[:insertion_start + len("# Write the target function here")]
    after_insertion = template_content[insertion_end:]

    # Combining all parts back together with the Python code inserted in between
    modified_template_content = before_insertion + "\n" + python_content + "\n" + after_insertion

    # Writing the modified content back to a new file
    if not os.path.exists(os.path.dirname(modified_file_path)):
        os.makedirs(os.path.dirname(modified_file_path))
    with open(modified_file_path, 'w') as file:
        file.write(modified_template_content)


def insert_code_str(code_str, template_file_path, modified_file_path, question_name):
    # Function to read the content of a file
    def read_file(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            return file.read()

    # Reading the contents of both files
    python_content = code_str
    # replace funcname
    python_content = replace_func_name(python_content, question_name)

    template_content = read_file(template_file_path)

    # Finding the position of the comments in the template file
    insertion_start = template_content.find("# Write the target function here")
    insertion_end = template_content.find("# End here", insertion_start)

    # Splitting the template content into two parts: before and after the insertion point
    before_insertion = template_content[:insertion_start + len("# Write the target function here")]
    after_insertion = template_content[insertion_end:]

    # Combining all parts back together with the Python code inserted in between
    modified_template_content = before_insertion + "\n" + python_content + "\n" + after_insertion

    # Writing the modified content back to a new file
    if not os.path.exists(os.path.dirname(modified_file_path)):
        os.makedirs(os.path.dirname(modified_file_path))
    with open(modified_file_path, 'w') as file:
        file.write(modified_template_content)


def insert_test_code(template_file_path, modified_file_path, question_num):
    # Function to read the content of a file
    def read_file(file_path):
        with open(file_path, 'r') as file:
            return file.read()

    insert_content = f"    question = {question_num}"
    template_content = read_file(template_file_path)

    # Finding the position of the comments in the template file
    insertion_start = template_content.find("# Write the unit tests here")
    insertion_end = template_content.find("# Unit tests end here", insertion_start)

    # Splitting the template content into two parts: before and after the insertion point
    before_insertion = template_content[:insertion_start + len("# Write the unit tests here")]
    after_insertion = template_content[insertion_end:]

    # Combining all parts back together with the Python code inserted in between
    modified_template_content = before_insertion + "\n" + insert_content + "\n" + after_insertion

    # Writing the modified content back to a new file
    with open(modified_file_path, 'w') as file:
        file.write(modified_template_content)


if __name__ == "__main__":
    question_num = 16
    template_path = "template\\template.py"
    answer_file_path = f'code\\{question_num}\\python'
    test_dir = f"unit_tests\\{question_num}"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    test_path = f"{test_dir}\\test.py"

    insert_code(answer_file_path, template_path, test_path, "minSizeSubarray")
    insert_test_code(test_path, test_path, question_num)