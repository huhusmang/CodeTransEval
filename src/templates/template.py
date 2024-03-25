# Write the declarations here
from collections import *
from typing import *
from math import *
from bisect import *
from itertools import *
from sortedcontainers import *
import itertools
import functools
import sys
import json
import ast
import math
import bisect
import collections
import sortedcontainers


sys.setrecursionlimit(2000)


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def create_list_from_array(arr):
    if not arr:
        return None

    head = ListNode(arr[0])
    current = head

    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next

    return head


def create_tree_from_list(lst):
    if not lst:
        return None

    root = TreeNode(lst[0])
    queue = deque([root])
    i = 1

    while i < len(lst):
        node = queue.popleft()
        if lst[i] is not None:
            node.left = TreeNode(lst[i])
            queue.append(node.left)
        i += 1
        if i < len(lst) and lst[i] is not None:
            node.right = TreeNode(lst[i])
            queue.append(node.right)
        i += 1

    return root


# Write the target function here

# End here


def serialize_list(obj) -> str:
    list_str = ["["]
    for item in obj:
        list_str.append(serialize_obj(item))
        list_str.append(",")
    list_str[-1] = "]"
    return "".join(list_str)


def serialize_dict(obj) -> str:
    m = OrderedDict(sorted(obj.items()))
    dict_str = ["{"]
    for key, value in m.items():
        dict_str.append(serialize_obj(key))
        dict_str.append(":")
        dict_str.append(serialize_obj(value))
        dict_str.append(",")
    dict_str[-1] = "}"
    return "".join(dict_str)


def linkedListToList(head):
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result


def serialize_obj(obj):
    if obj is None:
        return "null"
    if isinstance(obj, int) or isinstance(obj, float):
        return "{0:.6f}".format(obj)
    if isinstance(obj, str):
        return '"' + obj + '"'
    if isinstance(obj, bool):
        return str(obj)
    if isinstance(obj, list):
        return serialize_list(obj)
    if isinstance(obj, dict):
        return serialize_dict(obj)
    if isinstance(obj, ListNode):
        return linkedListToList(obj)
    raise Exception("Unrecognized Type!")


def are_equivalent(o1, o2) -> bool:
    a = serialize_obj(o1)
    b = serialize_obj(o2)
    print(str(a) + " " + str(b))
    return a == b


def convert_to_type(input_data, data_type):
    if data_type == "int":
        return int(input_data)
    elif data_type == "float":
        return float(input_data)
    elif data_type == "bool":
        if input_data == "true":
            return True
        elif input_data == "false":
            return False
    elif data_type == "str":
        if input_data == '""' or input_data == "''":
            return ""
        else:
            return input_data
    elif data_type == "List[int]":
        return list(ast.literal_eval(input_data))
    elif data_type == "List[List[int]]":
        return list(ast.literal_eval(input_data))
    elif data_type == "List[str]":
        return list(ast.literal_eval(input_data))
    elif data_type == "List[List[str]]":
        return list(ast.literal_eval(input_data))
    elif data_type == "TreeNode":
        input_data = input_data.replace("null", "None")
        return create_tree_from_list(list(ast.literal_eval(input_data)))
    elif data_type == "ListNode":
        return create_list_from_array(list(ast.literal_eval(input_data)))
    else:
        raise Exception("Unrecognized Type!")


def gen_testcases(question):
    testcases = []

    with open("/home/huhu/work/CodeTransSecEval/datas/function/datas.json", "r", encoding="utf-8") as file:
        datas = json.load(file)
    input_type = datas[question - 1]["params"]["python"]["paramsType"]

    for folder in range(1, 6):
        with open(f"/home/huhu/work/CodeTransSecEval/datas/function/testcases/{question}/{folder}i.txt", "r") as f:
            input_datas = f.readlines()

        for i, data_type in enumerate(input_type):
            input_datas[i] = convert_to_type(input_datas[i].strip("\n"), data_type)

        with open(f"/home/huhu/work/CodeTransSecEval/datas/function/testcases/{question}/{folder}o.txt", "r") as f:
            return_datas = f.readlines()[0]
        return_datas = convert_to_type(
            return_datas.strip("\n"),
            datas[question - 1]["params"]["python"]["returnType"],
        )

        testcases.append((input_datas, return_datas))

    return testcases


def start():
    count = 0
    total = 0
    # Write the unit tests here

    # Unit tests end here
    testcases = gen_testcases(question)
    for i, testcase in enumerate(testcases):
        total += 1
        input_datas, return_datas = testcase
        try:
            ans = testfunc(*input_datas)
            if are_equivalent(ans, return_datas):
                count += 1
            else:
                print(f"Testcase {i+1} Failed!")
        except Exception as e:
            print(f"Exception: {e}")
    if count == total:
        print("All Passed!")
    else:
        print(f"Passed {count}/{total} testcases!")
        print("Test Failed!")


if __name__ == "__main__":
    start()
