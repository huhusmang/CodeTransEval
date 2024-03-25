import csv
import pathlib

csv_base_path = pathlib.Path("/home/huhu/work/CodeTransSecEval/data/results/")
model = "gpt4_safe"
model_csv_path = csv_base_path / f"{model}"

results = []
for csv_file in sorted(model_csv_path.iterdir()):
    if csv_file.suffix == ".csv":
        id = csv_file.stem
        with open(csv_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                row.insert(0, id)
                results.append(row)

header = ["ID", "Name", "Description", "Severity", "Message", "Path", "Start line", "Start column", "End line", "End column"]
with open(csv_base_path / f"{model}.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(results)

# %%
import csv

ids = set()
with open("/home/huhu/work/CodeTransSecEval/data/results/gpt4.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        ids.add(row[0])

print(len(ids))
# %%
