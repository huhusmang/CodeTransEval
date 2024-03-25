#!/bin/bash

run_task() {
    local model_name=$1
    local task_type=$2
    local script_name=$3
    local language=$(echo "$task_type" | cut -d'_' -f2)
    local log_dir="/home/ubuntu/test_codellm/logs/${model_name}/${task_type}"
    local current_time=$(date +"%Y%m%d_%H%M%S")
    local filename="${log_dir}/run_all_${script_name}_${current_time}.log"
    local suffix
    if [ "$language" = "python" ]; then
        suffix="py"
    elif [ "$language" = "java" ]; then
        suffix="java"
    elif [ "$language" = "c++" ]; then
        suffix="cpp"
    fi

    [ ! -d "$log_dir" ] && mkdir -p "$log_dir"

    nohup python3 "${script_name}.py" \
        --start 1 \
        --end 101 \
        --template_path "/home/ubuntu/test_codellm/template/template.${suffix}" \
        --answer_json_path "/home/ubuntu/test_codellm/result/${model_name}/${task_type}/prediction.json" \
        --unit_tests_path "/home/ubuntu/test_codellm/unit_tests/${model_name}/${task_type}/test.${suffix}" \
        --results_path "/home/ubuntu/test_codellm/result/${model_name}/${task_type}/results.json" \
        --json_file_path "/home/ubuntu/test_codellm/datas/datas.json" \
        --prediction_num 1 \
        > "${filename}" 2>&1 &
}

# run_task "gpt4" "python_java" "run_all_java_json"
# run_task "wenxin" "java_python" "run_all_python_json"
# run_task "wenxin" "c++_python" "run_all_python_json"
# run_task "wenxin" "c++_java" "run_all_java_json"
# run_task "wenxin" "python_c++" "run_all_cpp_json"
# run_task "wenxin" "java_c++" "run_all_cpp_json"


declare -A tasks
tasks["python_java"]="run_all_java_json"
tasks["c++_java"]="run_all_java_json"
tasks["java_python"]="run_all_python_json"
tasks["c++_python"]="run_all_python_json"
tasks["python_c++"]="run_all_cpp_json"
tasks["java_c++"]="run_all_cpp_json"


model="codellama"
for key in "${!tasks[@]}"; do
    task=${tasks[$key]}

    echo "Running: run_task \"$model\" \"$key\" \"$task\""
    run_task "$model" "$key" "$task"

    # Wait five minutes after the command.
    sleep 300
done
echo "All tasks have been submitted"
sleep 300


# model="qwen"
# for key in "${!tasks[@]}"; do
#     task=${tasks[$key]}

#     echo "Running: run_task \"$model\" \"$key\" \"$task\""
#     run_task "$model" "$key" "$task"

#     # Wait five minutes after the command.
#     sleep 300
# done
# echo "All tasks have been submitted"
# sleep 300


# model="wenxin"
# for key in "${!tasks[@]}"; do
#     task=${tasks[$key]}

#     echo "Running: run_task \"$model\" \"$key\" \"$task\""
#     run_task "$model" "$key" "$task"

#     # Wait five minutes after the command.
#     sleep 300
# done
# echo "All tasks have been submitted"
# sleep 300


# model="minimax"
# for key in "${!tasks[@]}"; do
#     task=${tasks[$key]}

#     echo "Running: run_task \"$model\" \"$key\" \"$task\""
#     run_task "$model" "$key" "$task"

#     # Wait five minutes after the command.
#     sleep 300
# done
# echo "All tasks have been submitted"
# sleep 300


# model="zhipu"
# for key in "${!tasks[@]}"; do
#     task=${tasks[$key]}

#     echo "Running: run_task \"$model\" \"$key\" \"$task\""
#     run_task "$model" "$key" "$task"

#     # Wait five minutes after the command.
#     sleep 300
# done
# echo "All tasks have been submitted"
# sleep 300


# model="wenxin_3.5"
# for key in "${!tasks[@]}"; do
#     task=${tasks[$key]}

#     echo "Running: run_task \"$model\" \"$key\" \"$task\""
#     run_task "$model" "$key" "$task"

#     # Wait five minutes after the command.
#     sleep 300
# done
# echo "All tasks have been submitted"
