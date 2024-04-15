from tree_sitter import Language, Parser


PYTHON_LANGUAGE = Language("tests/build/my-languages.so", "python")

parser = Parser()
parser.set_language(PYTHON_LANGUAGE)


def find_function_nodes(node):
    if node.type == "function_definition":
        yield node

    if node == root_node:
        for child in node.children:
            yield from find_function_nodes(child)


def find_inner_function_nodes(node):
    if node.type == "function_definition":
        yield node
    for child in node.children:
        yield from find_inner_function_nodes(child)


def find_call_nodes(node):
    if node.type == "call":
        yield node
    for child in node.children:
        yield from find_call_nodes(child)


def get_node_text(node, code):
    start = node.start_byte
    end = node.end_byte
    return code[start:end]


with open("tests/file.py", "r") as f:
    code = f.read()
tree = parser.parse(bytes(code, "utf-8"))
root_node = tree.root_node

function_nodes_dict = {}
function_nodes_call_dict = {}
inner_function_nodes_dict = {}
function_nodes = list(find_function_nodes(root_node))
for func_node in function_nodes:
    # Extracting function name and code
    name_node = func_node.child_by_field_name("name")
    func_name = get_node_text(name_node, code)
    func_code = get_node_text(func_node, code)
    function_nodes_dict[func_name] = func_code

    # Extracting function calls
    call_nodes = list(find_call_nodes(func_node))
    call_node_name_list = []
    for call_node in call_nodes:
        call_name_node = call_node.child_by_field_name("function")
        if call_name_node is not None:
            call_name = get_node_text(call_name_node, code)
            call_node_name_list.append(call_name)
    function_nodes_call_dict[func_name] = call_node_name_list

    # Extracting inner functions
    inner_function_nodes = list(find_inner_function_nodes(func_node))
    inner_node_name_list = []
    for inner_func_node in inner_function_nodes:
        inner_name_node = inner_func_node.child_by_field_name("name")
        if inner_name_node is not None:
            inner_func_name = get_node_text(inner_name_node, code)
            if inner_func_name != func_name:
                inner_node_name_list.append(inner_func_name)
    inner_function_nodes_dict[func_name] = inner_node_name_list


print(function_nodes_dict)
print(function_nodes_call_dict)
print(inner_function_nodes_dict)

all_called_function_names = set()
for func_name in function_nodes_call_dict:
    for call_name in function_nodes_call_dict[func_name]:
        if call_name in function_nodes_dict and call_name != func_name:
            all_called_function_names.add(call_name)
print(all_called_function_names)

all_function_names = set(function_nodes_dict.keys())
entry_point = (all_function_names - all_called_function_names).pop()

def extracted_relevant_functions(function_nodes_dict, function_nodes_call_dict, entry_point, seen=None):
    if seen is None:
        seen = set()
    if entry_point in seen:
        return []
    seen.add(entry_point)

    extracted_functions = [function_nodes_dict[entry_point]]

    for call_name in function_nodes_call_dict[entry_point]:
        if call_name in function_nodes_dict:
            extracted_functions.extend(extracted_relevant_functions(function_nodes_dict, function_nodes_call_dict, call_name, seen))

    return extracted_functions

extracted_functions = extracted_relevant_functions(function_nodes_dict, function_nodes_call_dict, entry_point)
print("\n".join(extracted_functions))