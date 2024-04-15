使用 tree-sitter 来解析 LLM 输出的代码

Prerequisite：
./build.sh

优势：使用 AST 能够准确的识别出所有的函数定义以及函数名、被调用的函数等，只需逻辑对就行。
问题：目前唯一存在的问题还是**主函数**识别的问题，默认只有一个主函数，并且排除掉 main, TreeNode, ListNode 等函数