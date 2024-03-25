import json
import pathlib

QL_base_path = "/home/huhu/codeql-home/codeql-repo/python/ql/src/Security"
to_change_cweid = {
    "CWE-099": "CWE-022",
    "CWE-113": "CWE-113",
    "CWE-259": "CWE-798",
    "CWE-287": "CWE-287",
    "CWE-400": "CWE-730",
}


def build_json(path: str):
    datas = []
    path = pathlib.Path(path)

    for cwe_dir in sorted(path.iterdir()):
        if cwe_dir.is_dir():
            cwe_id = cwe_dir.name
            if cwe_id in to_change_cweid:
                Check_ql = QL_base_path + "/" + to_change_cweid[cwe_id]
            else:
                Check_ql = QL_base_path + "/" + cwe_id

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
                    data_dict["Check_ql"] = Check_ql

                    datas.append(data_dict)

    with open("/home/huhu/work/CodeTransSecEval/data/datas.json", "w") as f:
        json.dump(datas, f, indent=4)


if __name__ == "__main__":
    build_json("/home/huhu/work/CodeTransSecEval/data/CWE_Data")
