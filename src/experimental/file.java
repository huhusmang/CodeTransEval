import java.util.*;

class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;

    TreeNode(int val) {
        this.val = val;
        this.left = null;
        this.right = null;
    }
}

public class file{
    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(7);
        root.right = new TreeNode(0);
        root.left.left = new TreeNode(7);
        root.left.right = new TreeNode(-8);
        System.out.println(maxLevelSum(root));
    }

    public static int maxLevelSum(TreeNode root) {
        List<Integer> sums = new ArrayList<>();
        dfs(root, 0, sums);
        return sums.indexOf(Collections.max(sums)) + 1;
    }

    public static void dfs(TreeNode node, int level, List<Integer> sums) {
        if (level == sums.size()) {
            sums.add(node.val);
        } else {
            sums.set(level, sums.get(level) + node.val);
        }
        if (node.left != null) {
            dfs(node.left, level + 1, sums);
        }
        if (node.right != null) {
            dfs(node.right, level + 1, sums);
        }
    }
}