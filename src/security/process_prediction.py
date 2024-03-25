import re
from pathlib import Path
from utils.util import load_json


def extract_code(raw_prediction, code_type):
    return re.findall(rf"```{code_type}\n(.*?)\n```", raw_prediction, re.DOTALL)


def extract_class_name(java_code):
    return re.search(r"public class (\w+)", java_code).group(1)


def write_file(path, content):
    path.write_text(content)


def create_full_pom_xml(dependencies, template_path):
    with open(template_path, "r") as file:
        pom_xml_template = file.read()
    return pom_xml_template.format(dependencies)


def process_predictions(data, base_path, template_path):
    for item in data:
        problem_id = item["problem_id"]
        raw_prediction = item["raw_prediction"]

        problem_path = base_path / problem_id
        problem_path.mkdir(parents=True, exist_ok=True)

        java_code_matches = extract_code(raw_prediction, "java")
        pom_xml_matches = extract_code(raw_prediction, "xml")

        if java_code_matches:
            class_name = extract_class_name(java_code_matches[0])
            java_file_path = problem_path / f"{class_name}.java"
            write_file(java_file_path, java_code_matches[0])

        if pom_xml_matches:
            full_pom_xml = create_full_pom_xml(pom_xml_matches[0], template_path)
            pom_xml_path = problem_path / "pom.xml"
            write_file(pom_xml_path, full_pom_xml)
        else:
            empty_dependencies = "<dependencies>\n</dependencies>"
            full_pom_xml = create_full_pom_xml(empty_dependencies, template_path)
            pom_xml_path = problem_path / "pom.xml"
            write_file(pom_xml_path, full_pom_xml)


def main():
    model = "gpt4_safe"
    template_path = "/home/huhu/work/CodeTransSecEval/src/template/pom_template.xml"
    data = load_json(f"/home/huhu/work/CodeTransSecEval/data/predictions/{model}.json")
    base_path = Path(f"/home/huhu/work/CodeTransSecEval/data/predictions/{model}")
    process_predictions(data, base_path, template_path)


if __name__ == "__main__":
    main()
