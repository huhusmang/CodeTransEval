#!/bin/bash

# unset http_proxy
# unset https_proxy


run_task() {
    local model_name=$1
    local task_type=$2
    local sl=$(echo "$task_type" | cut -d'_' -f1)
    local tl=$(echo "$task_type" | cut -d'_' -f2)
    local log_dir="/home/ubuntu/test_codellm/logs/${model_name}/${task_type}"
    local current_time=$(date +"%Y%m%d_%H%M%S")
    local filename="${log_dir}/gen_prediction_${model_name}_${task_type}_${current_time}.log"

    # 检查日志目录是否存在，如果不存在则创建
    [ ! -d "$log_dir" ] && mkdir -p "$log_dir"

    nohup python3 "gen_prediction.py" \
        --start 1 \
        --end 101 \
        --model_name ${model_name} \
        --sl ${sl} \
        --tl ${tl} \
        --prediction_base_path /home/ubuntu/test_codellm/result/${model_name}/${task_type} \
        --json_path /home/ubuntu/test_codellm/result/${model_name}/${task_type}/prediction.json \
        --jsonl_path /home/ubuntu/test_codellm/result/${model_name}/${task_type}/prediction.jsonl \
        --answer_base_path /home/ubuntu/test_codellm/datas/gold_answer/ \
        --prediction_nums 1 \
        --datas_path /home/ubuntu/test_codellm/datas/datas.json \
        > "${filename}" 2>&1 &
}

# zhipu, minimax, spark, wenxin, qwen

# run_task "gpt4" "python_java"
# echo "start run gpt4 python_java"
# run_task "gpt4" "java_python"
# sleep 3600
# echo "start run gpt4 c++_python"
# run_task "gpt4" "c++_python"
# sleep 3600
# echo "start run gpt4 python_c++"
run_task "gpt4" "python_c++"
# sleep 3600
# echo "start run gpt4 c++_java"
# run_task "gpt4" "c++_java"
# sleep 3600
# echo "start run gpt4 java_c++"
# run_task "gpt4" "java_c++"
# sleep 3600

# unset http_proxy
# unset https_proxy

# echo "start run chatglm3 python_java"
# run_task "chatglm3" "python_java"
# sleep 3600
# echo "start run chatglm3 java_python"
# run_task "chatglm3" "java_python"
# sleep 3600
# echo "start run chatglm3 c++_python"
# run_task "chatglm3" "c++_python"
# sleep 3600
# echo "start run chatglm3 python_c++"
# run_task "chatglm3" "python_c++"
# sleep 3600
# echo "start run chatglm3 c++_java"
# run_task "chatglm3" "c++_java"
# sleep 3600
# echo "start run chatglm3 java_c++"
# run_task "chatglm3" "java_c++"

# nohup ./gen.sh > gen.log 2>&1 &

# run_task "spark" "python_java"
# run_task "spark" "java_python"
# run_task "spark" "c++_python"
# run_task "spark" "python_c++"
# run_task "spark" "c++_java"
# run_task "spark" "java_c++"

# run_task "wenxin" "python_java"
# run_task "wenxin" "java_python"
# run_task "wenxin" "c++_python"
# run_task "wenxin" "python_c++"
# run_task "wenxin" "c++_java"
# run_task "wenxin" "java_c++"

# run_task "qwen" "python_java"
# run_task "qwen" "java_python"
# run_task "qwen" "c++_python"
# run_task "qwen" "python_c++"
# run_task "qwen" "c++_java"
# run_task "qwen" "java_c++"

# run_task "zhipu" "python_java"
# run_task "zhipu" "java_python"
# run_task "zhipu" "c++_python"
# run_task "zhipu" "python_c++"
# run_task "zhipu" "c++_java"
# run_task "zhipu" "java_c++"

# run_task "minimax" "python_java"
# run_task "minimax" "java_python"
# run_task "minimax" "c++_python"
# run_task "minimax" "python_c++"
# run_task "minimax" "c++_java"
# run_task "minimax" "java_c++"


# projects=("spark" "wenxin" "qwen" "zhipu" "minimax")
# tasks=("python_java" "java_python" "c++_python" "python_c++" "c++_java" "java_c++")

# for project in "${projects[@]}"; do
#     for task in "${tasks[@]}"; do
#         run_task "$project" "$task"
#     done
# done