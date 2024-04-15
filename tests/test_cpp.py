from tree_sitter import Language, Parser


LANGUAGE = Language("tests/build/my-languages.so", "cpp")

parser = Parser()
parser.set_language(LANGUAGE)


def find_function_nodes(node):
    if node.type == "function_definition":
        yield node

    for child in node.children:
        yield from find_function_nodes(child)


def get_node_text(node, code):
    start = node.start_byte
    end = node.end_byte
    return code[start:end]


def find_call_nodes(node):
    if node.type == "call_expression":
        yield node
    for child in node.children:
        yield from find_call_nodes(child)


with open("tests/file.cpp", "r") as file:
    code = file.read()

tree = parser.parse(bytes(code, "utf-8"))
root_node = tree.root_node

function_nodes_dict = {}
function_nodes_call_dict = {}
function_nodes = list(find_function_nodes(root_node))
for func_node in function_nodes:
    func_name = ""

    for child in func_node.children:
        if child.type == "function_declarator":
            declarator_node = child
            for subchild in declarator_node.children:
                if subchild.type == "identifier" or subchild.type == "field_identifier":
                    func_name = get_node_text(subchild, code)
                    break

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

print(function_nodes_dict)
print(function_nodes_call_dict)


all_called_function_names = set()
for func_name in function_nodes_call_dict:
    for call_name in function_nodes_call_dict[func_name]:
        if call_name in function_nodes_dict and call_name != func_name:
            all_called_function_names.add(call_name)
print(all_called_function_names)

all_function_names = set(function_nodes_dict.keys())
special_function_names = set(['TreeNode', 'main'])
entry_point = (all_function_names - all_called_function_names - special_function_names).pop()

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
