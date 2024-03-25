import os
import json
from utils.util import replace_func_name


def insert_code(file_path, template_file_path, modified_file_path, question_name):
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()

    java_content = read_file(file_path)
    java_content = replace_func_name(java_content, question_name)
    template_content = read_file(template_file_path)

    insertion_start = template_content.find("// Write the target function here")
    insertion_end = template_content.find("// End here", insertion_start)

    before_insertion = template_content[
        : insertion_start + len("// Write the target function here")
    ]
    after_insertion = template_content[insertion_end:]

    modified_template_content = (
        before_insertion + "\n" + java_content + "\n" + after_insertion
    )

    if not os.path.exists(os.path.dirname(modified_file_path)):
        os.makedirs(os.path.dirname(modified_file_path))
    with open(modified_file_path, "w") as file:
        file.write(modified_template_content)


def insert_code_str(code_str, template_file_path, modified_file_path, question_name):
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()

    java_content = code_str

    java_content = java_content.replace(question_name, "testfunc")
    template_content = read_file(template_file_path)

    insertion_start = template_content.find("// Write the target function here")
    insertion_end = template_content.find("// End here", insertion_start)

    before_insertion = template_content[
        : insertion_start + len("// Write the target function here")
    ]
    after_insertion = template_content[insertion_end:]

    modified_template_content = (
        before_insertion + "\n" + java_content + "\n" + after_insertion
    )

    if not os.path.exists(os.path.dirname(modified_file_path)):
        os.makedirs(os.path.dirname(modified_file_path))
    with open(modified_file_path, "w") as file:
        file.write(modified_template_content)


def generate_test_code(input_types, output_type, question_number):
    code_template = """
        String[] input_type = {input_types_array};
        String output_type = "{output_type}";

        {input_declarations}
        {output_type} return_data;
        {output_type} gold_ans;

        String basePath = "/home/huhu/work/CodeTransSecEval/datas/function/testcases/{question_number}";
        for (int folder = 1; folder <= 5; folder++) {{
            total += 1;

            String[] inputDatas;
            try (BufferedReader br = new BufferedReader(new FileReader(Paths.get(basePath, folder + "i.txt").toString()))) {{
                inputDatas = br.lines().toArray(String[]::new);
            }} catch (FileNotFoundException e) {{
                throw new RuntimeException(e);
            }} catch (IOException e) {{
                throw new RuntimeException(e);
            }}
            {data_assignments}

            String returnDatas = null;
            try (BufferedReader br = new BufferedReader(new FileReader(Paths.get(basePath, folder + "o.txt").toString()))) {{
                returnDatas = br.readLine();
            }} catch (IOException e) {{
                e.printStackTrace();
            }}
            gold_ans = ({output_type})convertToType(returnDatas.trim(), output_type);

            try {{
                return_data = testfunc({parameters});
                if (areEquivalent(return_data, gold_ans)){{
                    count += 1;
                }}else{{
                    System.out.println("Testcase No." + folder + " Failed!");
                }}
            }} catch (Exception e) {{
                e.printStackTrace();
            }}
        }}
    """
    input_types_array = "{" + ", ".join([f'"{t}"' for t in input_types]) + "}"

    input_declarations = "\n\t\t".join(
        [
            f"{type_name} data{index};"
            for index, type_name in enumerate(input_types, start=1)
        ]
    )

    data_assignments = "\n\t\t".join(
        [
            f"data{index} = ({type_name})convertToType(inputDatas[{index - 1}].trim(), input_type[{index - 1}]);"
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
    )


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


if __name__ == "__main__":
    question_num = 94

    with open("/home/huhu/work/CodeTransSecEval/datas/function/datas.json", "r", encoding="utf-8") as file:
        datas = json.load(file)
    input_type = datas[question_num - 1]["params"]["java"]["paramsType"]
    output_type = datas[question_num - 1]["params"]["java"]["returnType"]

    template_path = "/home/huhu/work/CodeTransSecEval/src/templates/template.java"
    answer_file_path = f"code\\{question_num}\\java"
    test_dir = f"unit_tests\\{question_num}"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    test_path = f"{test_dir}\\test.java"

    insert_code(
        answer_file_path,
        template_path,
        test_path,
        datas[question_num - 1]["entry_point"],
    )
    code = generate_test_code(input_type, output_type, question_num)
    insert_testcases(code, test_path, test_path)
