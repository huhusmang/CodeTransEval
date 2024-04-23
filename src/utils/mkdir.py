import pathlib


def get_all_file_name(path):
    p = pathlib.Path(path)

    return [x.name for x in p.iterdir() if x.is_file()]


def create_dir_by_list(path, dir_list):
    p = pathlib.Path(path)
    for dir_name in dir_list:
        dir_path = p / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
    return


def create_files(path):
    p = pathlib.Path(path)
    for dir_name in p.iterdir():
        if dir_name.is_dir():
            for i in range(1, 6):
                sub_dir = dir_name / str(i)
                sub_dir.mkdir(parents=True, exist_ok=True)
                (sub_dir / "vul.py").touch()
                (sub_dir / "sec.py").touch()
                (sub_dir / "source").touch()
    return


# path = "samples/SecurityEval"
# file_names = get_all_file_name(path)
# CWE_IDS = sorted(list(set(x.split("_")[0] for x in file_names)))

# parent_path = pathlib.Path("CWE_Data")
# create_dir_by_list(parent_path, CWE_IDS)

path = "CWE_Data"
create_files(path)