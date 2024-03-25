# %%
import pathlib



result_path = pathlib.Path("/home/huhu/work/CodeTransSecEval/data/results/original")

results = {}
for file in sorted(result_path.iterdir()):
    if file.is_file():
        cwe = file.name
        with open(file, "r") as f:
            file_indexs = []
            for line in f:
                if "vul.py" in line:
                    file_index = line.split(",")[-5]
                    file_indexs.append(file_index)
            results[cwe] = file_indexs

a = [len(i) for i in results.values()]

# %%
