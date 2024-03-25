#include <string>
#include <vector>
#include <sstream>
#include <variant>
#include <iostream>
#include <algorithm>
#include <iterator>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <set>
#include <numeric>
#include <map>
#include <unordered_map>
#include <unordered_set>
#include <ranges>
#include <any>
#include <queue>
#include <climits>
#include <fstream>
#include <filesystem>
#include <stack>
#include <list>
#include <bitset>


using namespace std;

class Test {
public:

    struct ListNode {
        int val;
        ListNode *next;
        ListNode() : val(0), next(nullptr) {}
        ListNode(int x) : val(x), next(nullptr) {}
        ListNode(int x, ListNode *next) : val(x), next(next) {}
    };

    struct TreeNode {
        int val;
        TreeNode *left;
        TreeNode *right;
        TreeNode() : val(0), left(nullptr), right(nullptr) {}
        TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
        TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
    };

    ListNode* createLinkedList(const string& s) {
        istringstream ss(s);
        string item;
        ListNode dummy(0);
        ListNode* current = &dummy;

        while (getline(ss, item, ',')) {
            int num = stoi(item);
            current->next = new ListNode(num);
            current = current->next;
        }

        return dummy.next;
    }

    static vector<int> linkedListToList(ListNode* head) {
        vector<int> list;
        ListNode* current = head;

        while (current != nullptr) {
            list.push_back(current->val);
            current = current->next;
        }

        return list;
    }

    TreeNode* createBinaryTree(const string& data) {
        if (data.empty()) {
            return nullptr;
        }

        stringstream ss(data);
        string item;
        getline(ss, item, ',');
        TreeNode* root = new TreeNode(stoi(item));
        queue<TreeNode*> queue;
        queue.push(root);

        while (!queue.empty()) {
            TreeNode* node = queue.front();
            queue.pop();

            if (getline(ss, item, ',') && item != "null") {
                TreeNode* leftChild = new TreeNode(stoi(item));
                node->left = leftChild;
                queue.push(leftChild);
            }

            if (getline(ss, item, ',') && item != "null") {
                TreeNode* rightChild = new TreeNode(stoi(item));
                node->right = rightChild;
                queue.push(rightChild);
            }
        }

        return root;
    }

    // Function to print the tree in a basic way (for testing purposes)
    void printTree(TreeNode* node) {
        if (!node) return;
        cout << node->val << " ";
        printTree(node->left);
        printTree(node->right);
    }

    using ConvertibleTypes = variant<char, TreeNode*, ListNode*, vector<string>, bool, int, string, vector<vector<int>>, vector<int>, vector<long long>, vector<long>, long, long long>;

    // Helper function to split a string by a delimiter
    vector<string> split(const string& s, char delimiter) {
        vector<string> tokens;
        string token;
        istringstream tokenStream(s);
        while (getline(tokenStream, token, delimiter)) {
            tokens.push_back(token);
        }
        return tokens;
    }

    // Helper function to trim whitespace from a string
    string trim(const string& str) {
        size_t first = str.find_first_not_of(' ');
        if (string::npos == first) {
            return str;
        }
        size_t last = str.find_last_not_of(' ');
        return str.substr(first, (last - first + 1));
    }

    ConvertibleTypes convertToType(const string& data, const string& type) {
        if (type == "char") {
            return data[0];
        } else if (type == "TreeNode*") {
            return createBinaryTree(data);
        } else if (type == "ListNode*") {
            return createLinkedList(data);
        } else if (type == "vector<string>") {
            string trimmedData = trim(data);
            if (trimmedData.front() == '[') {
                trimmedData = trimmedData.substr(1, trimmedData.length() - 2);
            }
            vector<string> result;
            istringstream iss(trimmedData);
            string token;
            while (getline(iss, token, ',')) {
                // Remove whitespace, quotes, and escape characters
                token = trim(token);
                if (!token.empty() && token.front() == '\"') {
                    token.erase(0, 1); // Remove the first quote
                }
                if (!token.empty() && token.back() == '\"') {
                    token.pop_back(); // Remove the last quote
                }
                result.push_back(token);
            }
            return result;
        } else if (type == "bool") {
            string trimmedData = trim(data);
            return trimmedData == "true" || trimmedData == "1";
        } else if (type == "int") {
            return stoi(trim(data));
        } else if (type == "string") {
            if (data == "''" || data == "\"\"") {
                    return "";
                }
            return data;
        } else if (type == "vector<vector<int>>") {
            string trimmedData = trim(data);
            trimmedData = trimmedData.substr(1, trimmedData.length() - 2); // Remove the outer brackets
            vector<vector<int>> result;
            for (const auto& row : split(trimmedData, ']')) {
                string cleanRow = trim(row);
                cleanRow.erase(remove(cleanRow.begin(), cleanRow.end(), '['), cleanRow.end());
                vector<int> intRow;
                for (const auto& val : split(cleanRow, ',')) {
                    if (!val.empty()) {
                        intRow.push_back(stoi(trim(val)));
                    }
                }
                if (!intRow.empty()) {
                    result.push_back(intRow);
                }
            }
            return result;
        } else if (type == "vector<int>") {
            string trimmedData = trim(data);
            if (trimmedData.front() == '[') {
                trimmedData = trimmedData.substr(1, trimmedData.length() - 2);
            }
            vector<int> result;
            for (const auto& val : split(trimmedData, ',')) {
                result.push_back(stoi(trim(val)));
            }
            return result;
        } else if (type == "vector<long long>") {
            string trimmedData = trim(data);
            if (trimmedData.front() == '[') {
                trimmedData = trimmedData.substr(1, trimmedData.length() - 2);
            }
            vector<long long> result;
            for (const auto& val : split(trimmedData, ',')) {
                result.push_back(stoll(trim(val)));
            }
            return result;
        } else if (type == "vector<long>") {
            string trimmedData = trim(data);
            if (trimmedData.front() == '[') {
                trimmedData = trimmedData.substr(1, trimmedData.length() - 2);
            }
            vector<long> result;
            for (const auto& val : split(trimmedData, ',')) {
                result.push_back(stol(trim(val)));
            }
            return result;
        } else if (type == "long"){
            return stol(trim(data));
        } else if (type == "long long") {
            return stoll(trim(data));
        } else {
            return {}; // Return empty variant (or handle error)
        }
    }

  template <typename T> static string serialize_obj_(T obj) {
    if constexpr (is_same_v<T, int>) {
      return to_string((int)obj);
    }
    if constexpr (is_same_v<T, long>) {
      return to_string((long)obj);
    }
    if constexpr (is_same_v<T, long long>) {
      return to_string((long long)obj);
    }
    if constexpr (is_same_v<T, double>) {
      return to_string((double)obj);
    }
    if constexpr (is_same_v<T, char>) {
      return "'" + string(1, (char)obj) + "'";
    }
    if constexpr (is_same_v<T, bool>) {
      return (bool)obj ? "true" : "false";
    }
    if constexpr (is_same_v<T, string>) {
      return "\"" + (string)obj + "\"";
    }
    if constexpr (is_same_v<T, ListNode*>) {
        return serialize_list_(linkedListToList(obj));
    }
    throw runtime_error("Error: Invalid Type");
  }

  template <typename T> static string serialize_obj_(vector<T> obj) {
    return serialize_list_(obj);
  }

  template <typename K, typename V>
  static string serialize_obj_(map<K, V> obj) {
    return serialize_dict_(obj);
  }

  template <typename K, typename V>
  static string serialize_obj_(unordered_map<K, V> obj) {
    return serialize_dict_(obj);
  }

  template <typename T> static string serialize_list_(vector<T> obj) {
    string list_str = "[";
    if constexpr (is_same<T, bool>::value) {
      for (auto item : obj) {
      list_str += serialize_obj_((bool)item);
      list_str += ",";
      }
    }
    else{
    for (auto &item : obj) {
      list_str += serialize_obj_(item);
      list_str += ",";
    }
    }
    list_str[list_str.length() - 1] = ']';
    return list_str;
  }

  template <typename K, typename V>
  static string serialize_dict_(map<K, V> obj) {
    string dict_str = "{";
    for (auto &[key, value] : obj) {
      dict_str += serialize_obj_(key);
      dict_str += ":";
      dict_str += serialize_obj_(value);
      dict_str += ",";
    }
    dict_str[dict_str.length() - 1] = '}';
    return dict_str;
  }

  template <typename K, typename V>
  static string serialize_dict_(unordered_map<K, V> obj) {
    auto m = map<K, V>();
    for (auto &[key, value] : obj) {
      m[key] = value;
    }
    return serialize_dict_(m);
  }

  template <typename T1, typename T2> static bool AreEquivalent(T1 o1, T2 o2) {
    cout << serialize_obj_(o1) << " " << serialize_obj_(o2) << endl;
    return serialize_obj_(o1) == serialize_obj_(o2);
  }


  // Write the target function here

  // End here
    void Start() {
    bool ret;
    int total = 0;
    int count = 0;
    // Write the unit tests here
        
    // Unit tests end here
    if (count == total) {
      cout << "All Passed!" << endl;
    } else {
        cout << "Passed " << count << "/" << total << " testcases!" << endl;
        cout << "Test Failed!" << endl;
    }
  }
};

int main() {
    Test test;
    test.Start();
    return 0;
}