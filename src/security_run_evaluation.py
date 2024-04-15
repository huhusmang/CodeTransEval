import pathlib
import re
import subprocess
import time
import argparse
from typing import List

from pydantic import BaseModel, Field

# Constants for paths that can be customized as needed
PYTHON_CODEQL_BASE_PATH = pathlib.Path(
    "/home/huhu/codeql-home/codeql-repo/python/ql/src"
)
JAVA_CODEQL_BASE_PATH = pathlib.Path("/home/huhu/codeql-home/codeql-repo/java/ql/src")
SCRIPTS_BASE_PATH = pathlib.Path("/home/huhu/work/CodeTransSecEval/scripts")
DATA_BASE_PATH = pathlib.Path("/home/huhu/work/CodeTransSecEval/datas/security")

# Mapping for CWE changes and experimental CWEs
PYTHON_CWE_CHANGES = {
    "CWE-020": PYTHON_CODEQL_BASE_PATH
    / "Security/CWE-020-ExternalAPIs/UntrustedDataToExternalAPI.ql",
    "CWE-208": PYTHON_CODEQL_BASE_PATH / "experimental/Security/CWE-208",
    "CWE-287": PYTHON_CODEQL_BASE_PATH
    / "experimental/Security/CWE-287-ConstantSecretKey",
    "CWE-338": PYTHON_CODEQL_BASE_PATH / "experimental/Security/CWE-338",
    "CWE-347": PYTHON_CODEQL_BASE_PATH / "experimental/Security/CWE-347",
    "CWE-348": PYTHON_CODEQL_BASE_PATH / "experimental/Security/CWE-348",
    "CWE-400": PYTHON_CODEQL_BASE_PATH / "Security/CWE-730",
    "CWE-614": PYTHON_CODEQL_BASE_PATH / "experimental/Security/CWE-614",
}

JAVA_CWE_CHANGES = {
    "CWE-020": JAVA_CODEQL_BASE_PATH
    / "Security/CWE/CWE-020/UntrustedDataToExternalAPI.ql",
    "CWE-078": JAVA_CODEQL_BASE_PATH / "experimental/Security/CWE/CWE-078",
    "CWE-094": JAVA_CODEQL_BASE_PATH / "experimental/Security/CWE/CWE-094",
    "CWE-208": JAVA_CODEQL_BASE_PATH / "experimental/Security/CWE/CWE-208",
    "CWE-348": JAVA_CODEQL_BASE_PATH / "experimental/Security/CWE/CWE-348",
    "CWE-400": JAVA_CODEQL_BASE_PATH / "Security/CWE/CWE-730",
}


class Config(BaseModel):
    model: str
    operation: str
    log_base_path: pathlib.Path = Field(default=DATA_BASE_PATH / "logs")
    dataset_base_path: pathlib.Path = Field(default=DATA_BASE_PATH / "predictions")
    database_base_path: pathlib.Path = Field(default=DATA_BASE_PATH / "databases")
    result_base_path: pathlib.Path = Field(default=DATA_BASE_PATH / "results")

    @property
    def languange(self) -> str:
        if self.model == "original":
            return "python"
        return "java"

    @property
    def dataset_path(self) -> pathlib.Path:
        # Only for original dataset testing
        if self.model == "original":
            return DATA_BASE_PATH / "datasets"
        return self.dataset_base_path / self.model

    @property
    def database_path(self) -> pathlib.Path:
        return self.database_base_path / self.model

    @property
    def result_path(self) -> pathlib.Path:
        return self.result_base_path / self.model

    @property
    def log_file_path(self) -> pathlib.Path:
        return self.log_base_path / f"{self.operation}_database_{self.model}.log"

    @property
    def script_path(self) -> pathlib.Path:
        return SCRIPTS_BASE_PATH / f"{self.operation}_database_{self.model}.sh"


def create_directory_if_not_exists(path: pathlib.Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def get_ql_query_path(cwe: str, model: str) -> str:
    # Only for original dataset testing
    if model == "original":
        cwe_changes = PYTHON_CWE_CHANGES
        codeql_base_path = PYTHON_CODEQL_BASE_PATH
        ql_query_path = codeql_base_path / "Security" / cwe
    else:
        cwe_changes = JAVA_CWE_CHANGES
        codeql_base_path = JAVA_CODEQL_BASE_PATH
        cwe = cwe[:-2]  # Convert format like CWE-020-1 to CWE-020
        ql_query_path = codeql_base_path / "Security" / "CWE" / cwe

    return str(cwe_changes.get(cwe, ql_query_path))


def generate_commands(configs: Config) -> List[str]:
    if configs.operation == "create":
        create_directory_if_not_exists(configs.database_path)
        commands = [
            f"codeql database create {configs.database_path / cwe_dir.name} --overwrite --language={configs.languange} --source-root={configs.dataset_path / cwe_dir.name}"
            for cwe_dir in sorted(configs.dataset_path.iterdir())
            if cwe_dir.is_dir()
        ]
        return commands
    elif configs.operation == "analyze":
        create_directory_if_not_exists(configs.result_path)
        commands = [
            f"codeql database analyze {configs.database_path / dir.name} --format=csv --output={configs.result_path / dir.name}.csv {get_ql_query_path(dir.name, configs.model)}"
            for dir in sorted(configs.database_path.iterdir())
            if dir.is_dir()
        ]
        return commands


def write_commands_to_script(commands: List[str], script_path: pathlib.Path) -> None:
    script_path.write_text("\n".join(commands))


def execute_script_and_log(
    script_path: pathlib.Path, log_file_path: pathlib.Path, model: str
) -> None:
    # Only for original dataset testing
    if model == "original":
        pattern = r"CWE-\d+"
    else:
        pattern = r"CWE-\d+-\d+"

    command_status = {}
    with log_file_path.open("w") as log_file:
        for command in script_path.read_text().splitlines():
            result = subprocess.run(
                command, shell=True, stdout=log_file, stderr=subprocess.STDOUT
            )
            cwe = re.search(pattern, command).group()
            status = "Success" if result.returncode == 0 else "Failed"
            command_status[cwe] = status
            print(f"{command} -> {status}")
            time.sleep(10)

        for cwe, status in command_status.items():
            log_file.write(f"{cwe}: {status}\n")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name", type=str, default="gpt4", help="Name of the model"
    )
    return parser.parse_args()


def main(operation: str = "create", only_execute: bool = False) -> None:
    args = parse_arguments()
    model = args.model_name
    configs = Config(model=model, operation=operation)
    if not only_execute:
        commands = generate_commands(configs)
        write_commands_to_script(commands, configs.script_path)
    execute_script_and_log(configs.script_path, configs.log_file_path, configs.model)


if __name__ == "__main__":
    operation = {
        "1": "create",
        "2": "analyze",
    }
    main(operation=operation["1"], only_execute=False)
    main(operation=operation["2"], only_execute=False)
