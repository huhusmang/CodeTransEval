# %%
import json
import matplotlib.pyplot as plt

with open("/home/huhu/work/CodeTransSecEval/datas/function/predictions/results.json", "r") as file:
    data = json.load(file)

# Extract Pass@1 rate for each model
pass_rates = {model["model"]: 
              [task["result"]["Pass@1 rate"] for task in model["tasks_results"]] 
              for model in data}

# Calculate average Pass@1 rate for each model
avg_pass_rates = {model: sum(rates) / len(rates) for model, rates in pass_rates.items()}

# Create bar chart
plt.figure(figsize=(8, 6))
plt.bar(avg_pass_rates.keys(), avg_pass_rates.values())
plt.xlabel("Model")
plt.ylabel("Average Pass@1 Rate")
plt.title("Overall Pass@1 Rate Comparison")
plt.show()



# %%
import json
import matplotlib.pyplot as plt
import numpy as np

with open("/home/huhu/work/CodeTransSecEval/datas/function/predictions/results.json", "r") as file:
    data = json.load(file)

# Extract Pass@1 rate for each task and model
tasks = ["c++_java", "python_c++", "c++_python", "java_python", "python_java", "java_c++"]
pass_rates = {}
for task in tasks:
    pass_rates[task] = {}
    for model in data:
        pass_rates[task][model["model"]] = model["tasks_results"][tasks.index(task)]["result"]["Pass@1 rate"]

# Create grouped bar chart
num_models = len(data)
num_tasks = len(data[0]["tasks_results"])
model_names = [model["model"] for model in data]
task_names = [task["task"] for task in data[0]["tasks_results"]]

width = 0.8 / num_models  # the width of the bars
x = np.arange(num_tasks)  # the label locations

fig, ax = plt.subplots(figsize=(12, 8))
rects = []
for i in range(num_models):
    model_pass_rates = [pass_rates[task][model_names[i]] for task in task_names]
    rects.append(ax.bar(x - width/2 + i*width, model_pass_rates, width, label=model_names[i]))

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Task')
ax.set_ylabel('Pass@1 Rate')
ax.set_title('Pass@1 Rate by Task and Model')
ax.set_xticks(x + 3.5 * width)
ax.set_xticklabels(task_names)
ax.legend()

fig.tight_layout()

plt.show()


# %%
# Stacked bar chart of Answer_type_nums: Show the distribution of answer types (all_passed, compilation_failed, etc.) for each model. This reveals the types of errors each model is prone to making.
import json
import matplotlib.pyplot as plt

with open("/home/huhu/work/CodeTransSecEval/datas/function/predictions/results.json", "r") as file:
    data = json.load(file)
# Extract answer type numbers for each model
answer_types = {model["model"]: 
                [task["result"]["Answer_type_nums"] for task in model["tasks_results"]] 
                for model in data}
# %%
# Create stacked bar chart
plt.figure(figsize=(8, 6))
bottom_pos = [0] * len(answer_types)
for answer_type in ["all_passed", "compilation_failed", "runtime_error", "wrong_answer", "timeout_error", "other_error"]:
    values = [sum(task[answer_type] for task in model_tasks) for model_tasks in answer_types.values()]
    plt.bar(answer_types.keys(), values, bottom=bottom_pos, label=answer_type)
    bottom_pos = [x + y for x, y in zip(bottom_pos, values)]

plt.xlabel("Model")
plt.ylabel("Number of Answers")
plt.title("Distribution of Answer Types")
plt.legend()
plt.show()

# %%
