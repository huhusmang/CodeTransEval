import json
import pathlib

PYTHON_CODEQL_BASE_PATH = pathlib.Path(
    "/home/huhu/codeql-home/codeql-repo/python/ql/src"
)
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


def build_json(path: str):
    datas = []
    path = pathlib.Path(path)

    for cwe_dir in sorted(path.iterdir()):
        if cwe_dir.is_dir():
            cwe_id = cwe_dir.name
            if cwe_id in PYTHON_CWE_CHANGES:
                Check_ql = PYTHON_CWE_CHANGES[cwe_id]
            else:
                Check_ql = PYTHON_CODEQL_BASE_PATH / cwe_id

            for subdir in sorted(cwe_dir.iterdir()):
                if subdir.is_dir():
                    data_dict = {
                        "ID": "",
                        "Description": "",
                        "VulCode": "",
                        "Check_ql": "",
                        "Source": "",
                    }
                    ID = cwe_id + "-" + subdir.name
                    with open(subdir / "vul.py", "r") as f:
                        VulCode = f.read()

                    with open(subdir / "source", "r") as f:
                        Source = f.read()

                    data_dict["ID"] = ID
                    data_dict["VulCode"] = VulCode
                    data_dict["Source"] = Source
                    data_dict["Check_ql"] = str(Check_ql)

                    datas.append(data_dict)

    with open("/home/huhu/work/CodeTransSecEval/datas/security/datas.json", "w") as f:
        json.dump(datas, f, indent=4)


if __name__ == "__main__":
    build_json("/home/huhu/work/CodeTransSecEval/datas/security/datasets")
