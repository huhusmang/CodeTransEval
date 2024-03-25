import os
from utils.util import replace_func_name


def insert_code(file_path, template_file_path, modified_file_path, question_name):
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()

    cpp_content = read_file(file_path)
    cpp_content = replace_func_name(cpp_content, question_name)
    template_content = read_file(template_file_path)

    insertion_start = template_content.find("// Write the target function here")
    insertion_end = template_content.find("// End here", insertion_start)

    before_insertion = template_content[
        : insertion_start + len("// Write the target function here")
    ]
    after_insertion = template_content[insertion_end:]

    modified_template_content = (
        before_insertion + "\n" + cpp_content + "\n" + after_insertion
    )

    if not os.path.exists(os.path.dirname(modified_file_path)):
        os.makedirs(os.path.dirname(modified_file_path))
    with open(modified_file_path, "w") as file:
        file.write(modified_template_content)


def insert_code_str(code_str, template_file_path, modified_file_path, question_name):
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()

    cpp_content = code_str

    # delete `public` or `static` if needed
    cpp_content = cpp_content.replace("public ", "").replace("static ", "").replace("private ", "").replace("protected ", "")

    cpp_content = cpp_content.replace(question_name, "testfunc")
    template_content = read_file(template_file_path)

    insertion_start = template_content.find("// Write the target function here")
    insertion_end = template_content.find("// End here", insertion_start)

    before_insertion = template_content[
        : insertion_start + len("// Write the target function here")
    ]
    after_insertion = template_content[insertion_end:]

    modified_template_content = (
        before_insertion + "\n" + cpp_content + "\n" + after_insertion
    )

    if not os.path.exists(os.path.dirname(modified_file_path)):
        os.makedirs(os.path.dirname(modified_file_path))
    with open(modified_file_path, "w") as file:
        file.write(modified_template_content)


def insert_testcases(code, template_file_path, modified_file_path):
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()

    template_content = read_file(template_file_path)

    insertion_start = template_content.find("// Write the unit tests here")
    insertion_end = template_content.find("// Unit tests end here", insertion_start)

    before_insertion = template_content[
        : insertion_start + len("// Write the unit tests here")
    ]
    after_insertion = template_content[insertion_end:]

    modified_template_content = before_insertion + "\n" + code + "\n" + after_insertion

    with open(modified_file_path, "w") as file:
        file.write(modified_template_content)


def generate_test_code(input_types, output_type, question_number):
    code_template = """
        string input_types[] = {{{input_types_array}}};
        string output_type = "{output_type}";

        {input_declarations}
        {output_type} return_data;
        {output_type} gold_ans;

        string basePath = "/home/huhu/work/CodeTransSecEval/datas/function/testcases/{question_number}/";
        for (int folder = 1; folder <= 5; folder++) {{
            total += 1;

            string inputDatas[{input_types_length}];
            ifstream fileInput(basePath + to_string(folder) + "i.txt");
            string line;
            int lineIndex = 0;
            while (getline(fileInput, line)) {{
                inputDatas[lineIndex++] = line;
            }}
            fileInput.close();

            {data_assignments}

            string returnDatas;
            ifstream fileOutput(basePath + to_string(folder) + "o.txt");
            if (getline(fileOutput, returnDatas)) {{
                gold_ans = get<{output_type}>(convertToType(returnDatas, output_type));
            }}
            fileOutput.close();

            try {{
                return_data = testfunc({parameters});                
                if (AreEquivalent(return_data, gold_ans)) {{
                    count += 1;
                }}else{{
                    cout << "Testcase No." << folder << " Failed!" << endl;
                }}
            }} catch (const exception& e) {{
                cout << "An exception occurred: " << e.what() << endl;
            }}
        }}
    """
    input_types_array = ", ".join([f'"{t}"' for t in input_types])

    input_declarations = "\n\t\t".join(
        [
            f"{type_name} data{index};"
            for index, type_name in enumerate(input_types, start=1)
        ]
    )

    data_assignments = "\n\t\t".join(
        [
            f"data{index} = get<{type_name}>(convertToType(inputDatas[{index - 1}], input_types[{index - 1}]));"
            for index, type_name in enumerate(input_types, start=1)
        ]
    )

    parameters = ", ".join([f"data{index}" for index in range(1, len(input_types) + 1)])

    return code_template.format(
        input_types_array=input_types_array,
        output_type=output_type,
        question_number=question_number,
        input_declarations=input_declarations,
        data_assignments=data_assignments,
        parameters=parameters,
        input_types_length=len(input_types),
    )


