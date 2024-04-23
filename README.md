# Code Translation Evaluator

## Introduction

Welcome to the Code Translation Evaluator, a tool designed to assess code translation models. In the ever-evolving landscape of machine learning and AI, the ability to accurately translate code across different programming languages is paramount. Our project addresses this need by providing a comprehensive, automated solution for evaluating the efficacy of code translation models.

### Key Functionalities

1. **Automated Model Output Retrieval:** At its core, the Code Translation Evaluator is equipped with the capability to automatically obtain outputs from various code translation models. This feature ensures seamless integration and a hassle-free approach to sourcing model outputs for evaluation.

2. **Standardized Code Formatting:** Recognizing the diversity in code structure and syntax, our tool adeptly extracts and transforms these model outputs into a standardized code format. This uniformity is crucial for accurate evaluation and comparison across different models.

3. **Robust Evaluation Mechanism:** The heart of our project lies in its powerful evaluation engine. It meticulously assesses the translated code, considering various aspects of accuracy, efficiency, and reliability. This automated process not only saves time but also introduces a level of precision and consistency in evaluation.

4. **Comprehensive Evaluation Metrics:** Understanding the multifaceted nature of code translation, the Code Translation Evaluator provides multiple evaluation indicators. These indicators offer a holistic view of the model's performance, covering aspects like syntactic correctness, semantic accuracy, and real-world applicability.

## Requirements
Tools that need to be installed:
```
Python 3.10
OpenJDK 17 (Java)
C++ 20
```
Install all required python dependencies:
```
codebleu
dashscope
numpy
qianfan
Requests
volcengine
websocket_client
zhipuai
```
Install all required python dependencies (you can skip this step if you have set up the dependencies before and the verisons are not strictly required):
```
pip install -r requirements.txt
```

## Running the Code Translation Evaluator

### ⚠️ Configuration ⚠️
Before starting, ensure to set up your environment:

1. **API Key Configuration:** Initialize your API key in the `models/config.py` file. This key is essential for accessing the model's functionalities.

2. **File Path Adjustments:** Modify the file paths in the following scripts to align with your local setup:
    - Update the `gen_testcases` function within `template/template.py`.
    - Adjust the `generate_test_code` function in `utils/gen_test_java.py`.
    - Modify the `generate_test_code` function in `utils/gen_test_cpp.py`.

### Generating the LLM Output
To obtain translation results from your model:

1. Run the `gen.sh` script. Customize the model and translation task as needed within this script.
2. The results will be saved in the `results` folder.

> **Note:** Ensure to update any file paths in the `gen.sh` script to match your local environment.

### Running Predictions
To execute model predictions:

1. Execute the `run.sh` script. Like before, you may need to customize the model and translation task in the script.
2. Output will be stored in the `results` folder.

> **Note:** Similar to the `gen.sh` script, confirm that all paths within `run.sh` are correctly set for your system.

### Obtaining Evaluation Metrics
To get the evaluation metrics such as pass@k and CodeBLEU:

1. Run the `eval.py` script. This will process the data and output the metrics.
2. Results will be found in the corresponding `results.json` file.
3. For an aggregated view of all results, run `utils/concat_all_results.py`.

## TODO
- [ ] Set up a global configuration named `config` to save various `base_path` values from the `datas`. 
- [ ] Remove the fixed file path in scripts.

## Acknowledgments
In this project, we have referenced the `TestRunner` component originally developed in the [G-TranSEval project](https://github.com/polyeval/g-transeval). We express our gratitude to the authors and contributors of the G-TranSEval project for their original work, which provided a solid foundation for our frame. 

Please refer to the [G-TranSEval repository](https://github.com/polyeval/g-transeval) for more information on their project and to view the original implementation of the TestRunner component.




