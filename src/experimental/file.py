from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def maxLevelSum(root: Optional[TreeNode]) -> int:
    sums = []
    dfs(root, 0, sums)
    testfunc()
    return sums.index(max(sums)) + 1


def dfs(node: TreeNode, level: int, sums) -> None:
    if level == len(sums):
        sums.append(node.val)
    else:
        sums[level] += node.val
    if node.left:
        dfs(node.left, level + 1, sums)
    if node.right:
        dfs(node.right, level + 1, sums)


def testfunc():
    print("Hello, World!")
    print("This is a test function.")
    testfunc()
    def testfunc2():
        print("This is a nested function.")
    testfunc2()


if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(7)
    root.right = TreeNode(0)
    root.left.left = TreeNode(7)
    root.left.right = TreeNode(-8)
    print(maxLevelSum(root))
