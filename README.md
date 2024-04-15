
1. 修改 model-name 为对应的版本
2. 修改图表的 bug
3. 增加一个清除按钮（加不加都行



重构 function 的代码

1. 配置一个全局的 config ，保存 datas 里的各种 base_path，剩下每个运行的脚本都要重新写

1. 提取所有的函数名
2. 去掉特殊的函数名
3. 提取到每个函数体
4. 在这些函数体的 lines 中找到被调用的函数名，剩下的就是主函数名
   1. 递归调用自己的是个特例
   2. 有多余的 main 函数等调用了主函数，也是特例


TODO: 修改 eval.py 中 answer_type = 0 的
1. 之前的 results.json 中有 answer_type = 0 的
/home/huhu/work/CodeTransEvalu/logs/spark/python_c++/run_all_run_all_cpp_json_20231212_104927.log
2023-12-12 10:52:17 INFO Running task: 97_0...
2023-12-12 10:52:19 INFO Running task: 98_0...
2023-12-12 10:52:21 INFO Test Failed!
2023-12-12 10:52:21 INFO run_output: b'true false\nTestcase No.1 Failed!\ntrue true\nfalse false\ntrue false\nTestcase No.4 Failed!\ntrue true\nPassed 3/5 testcases!\nTest Failed!\n'

It looks like you're encountering a "Segmentation fault" error when running a program (presumably a C or C++ executable named `out.o`). **This error occurs when a program tries to access a memory segment that it's not allowed to, which often happens due to issues like dereferencing a null or uninitialized pointer, accessing memory out of bounds of allocated memory, or corrupting memory in some way.**

The input you've shown (`22 22` and `0 0`) could be related to how your program is handling input values, but without seeing the code, it's challenging to provide a precise solution. However, here are some general steps to diagnose and fix segmentation faults:

1. **Check Pointer Usage**: Ensure all pointers are initialized before use and check that you're not dereferencing null or dangling pointers (pointers pointing to deallocated memory).

2. **Array Bounds**: Verify that all array accesses are within the bounds of the array. Accessing an array out of its bounds is a common cause of segmentation faults.

3. **Use Debugging Tools**: Tools like `gdb` (GNU Debugger) can help identify where the segmentation fault occurs. Running your program through `gdb` and using the `run` command with your input, followed by `bt` (backtrace) after the crash, can provide valuable insight into the source of the error.

4. **Memory Management**: If your program dynamically allocates memory (using `malloc`, `calloc`, or `new`), ensure that every allocated memory is correctly freed or deleted when it's no longer needed. Memory leaks or double free errors can lead to unpredictable behavior.

5. **Buffer Overflows**: Be cautious with operations that write to memory, such as string copying or manipulation functions. Ensure that buffers are large enough to hold any data written to them.

6. **Static Analysis Tools**: Tools like `valgrind` or static analyzers (e.g., Clang Static Analyzer for C/C++) can help detect memory mismanagement, use of uninitialized memory, and other issues that could lead to segmentation faults.

If you need more specific advice, feel free to share a snippet of the code where you suspect the issue might be, or describe what the program is supposed to do with the input it receives.


wenxin_3.5/c++_python:93
python3 ./test.py 
1.000000 1.000000
0.000000 0.000000
Killed


The message "Killed" after running your Python script, `test.py`, with the provided inputs suggests that the script was terminated unexpectedly. This termination could be due to several reasons, including but not limited to:

1. **Memory Overuse**: The script might be consuming too much memory, leading the system's Out Of Memory (OOM) killer to terminate it to protect system stability. This is common in scenarios where the script enters an infinite loop that allocates memory (like appending to a list without end) or tries to create a data structure that's too large for the available memory.

2. **Time Limit Exceeded**: If you're running this script on a platform with execution time limits (like some online IDEs or managed computing environments), it might be killed once it exceeds the allowed execution time.

3. **Explicit Signal**: The script might receive a termination signal from the system or another process, such as SIGKILL (`kill -9 <pid>`), which immediately terminates the process without cleanup.

4. **Resource Limitation**: On Unix-like systems, resource limits set with `ulimit` or similar tools can cause processes to be killed if they exceed allowed usage for resources like CPU time, file sizes, or number of processes/threads.

To diagnose and fix the issue, consider the following approaches:

- **Check System Logs**: System logs can provide clues. On Linux, for example, the `dmesg` command might show messages from the OOM killer.

- **Resource Monitoring**: Use tools like `top`, `htop`, or `free` to monitor your system's resource usage while the script is running. This can help you identify if it's consuming excessive resources.

- **Debugging and Profiling**: Use Python's debugging tools (like `pdb`) or profiling tools (`cProfile` or `memory_profiler`) to trace the script's execution and identify where resources are being used excessively.

- **Review Code for Infinite Loops/Allocations**: Look for any loops or recursive calls that might not terminate correctly or any operations that could allocate large amounts of memory (like generating a large list or dictionary).

- **Limit Resources**: If applicable, limit the script's resource usage explicitly. Python doesn't have built-in mechanisms for this, but you can manage it at the system level with `ulimit` (on Unix-like systems) or within your script by carefully managing memory use and execution time.

If you have a specific part of the code you're unsure about, or if you can describe what the script is intended to do, I can provide more targeted advice.