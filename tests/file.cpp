#include <vector>
#include <algorithm>
using namespace std;

// Definition for a binary tree node.
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(NULL), right(NULL) {}
};

class Solution {
public:
    int maxLevelSum(TreeNode* root) {
        vector<int> sums;
        dfs(root, 0, sums);
        testfunc();
        return max_element(sums.begin(), sums.end()) - sums.begin() + 1;
    }

private:
    void dfs(TreeNode* node, int level, vector<int>& sums) {
        if (level == sums.size()) {
            sums.push_back(node->val);
        } else {
            sums[level] += node->val;
        }
        if (node->left) {
            dfs(node->left, level + 1, sums);
        }
        if (node->right) {
            dfs(node->right, level + 1, sums);
        }
    }

    void testfunc() {
        // Implement your test function here
    }
};