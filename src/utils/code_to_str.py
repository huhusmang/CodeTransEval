import os


def convert_python_code(code: str):
    single_line_code = code.replace("\n", "\\n").replace('"', "'")
    return single_line_code


def convert_javaC_code(code: str):
    single_line_code = (
        code.replace("\n", " ").replace("    ", "").replace('"', "'").replace("\t", "")
    )
    return single_line_code


def remove_trailing_blank_lines(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    while lines and not lines[-1].strip():
        lines.pop()

    if lines and lines[-1].endswith("\n"):
        lines[-1] = lines[-1].rstrip("\n")

    with open(file_path, "w") as file:
        file.writelines(lines)


def all_files(code_folder):
    single_line_code_lists = []
    for folder_num in range(1, 101):
        subfolder_path = os.path.join(code_folder, str(folder_num))
        # py_path = os.path.join(subfolder_path, "python")
        # java_path = os.path.join(subfolder_path, "java")
        c_path = os.path.join(subfolder_path, "c")

        # remove_trailing_blank_lines(py_path)
        # remove_trailing_blank_lines(java_path)
        remove_trailing_blank_lines(c_path)

        with open(c_path, "r", encoding="utf-8") as f:
            code = f.read()
        single_line_code = convert_javaC_code(code)

        single_line_code_lists.append(single_line_code)

    save_path = os.path.join(code_folder, "c.txt")
    with open(save_path, "w", encoding="utf-8") as f:
        f.write("\n".join(single_line_code_lists))


if __name__ == "__main__":
    # code_folder = "/home/ubuntu/test_codellm/datas/gold_answer/"
    # all_files(code_folder)
    base_path = "/home/ubuntu/test_codellm/datas/testcases/"
    for folder_num in range(20, 101):
        dir_ = os.path.join(base_path, str(folder_num))
        for i in range(1, 6):
            in_txt = os.path.join(dir_, str(i) + "i.txt")
            out_txt = os.path.join(dir_, str(i) + "o.txt")

            remove_trailing_blank_lines(in_txt)
            remove_trailing_blank_lines(out_txt)


