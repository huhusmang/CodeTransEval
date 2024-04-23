# %%
from pathlib import Path


def count_innermost_subdirectories(parent_dir):
    """Count the total number of innermost subdirectories within a given directory."""
    parent_path = Path(parent_dir)
    innermost_dirs_count = 0

    for root_dir in parent_path.iterdir():  # Recursively go through all directories
        if root_dir.is_dir():
            innermost_dirs_count += len(list(root_dir.iterdir()))

    return innermost_dirs_count

# Example usage
count = count_innermost_subdirectories('/home/huhu/work/CodeTransSecEval/data/CWE_Data')
print(f"Total number of innermost subdirectories: {count}")  # 70

# %%
def list_subdirectories_with_count(parent_dir):
    """List subdirectories and their counts of innermost subdirectories."""
    parent_path = Path(parent_dir)
    subdir_counts = []

    for subdir in parent_path.iterdir():
        if subdir.is_dir():  # Only process directories
            count = 0  # Count of innermost subdirectories
            for root_dir in subdir.rglob('*'):  # Recursively go through all directories within the subdir
                if root_dir.is_dir() and not any(child.is_dir() for child in root_dir.iterdir()):
                    count += 1
            subdir_counts.append((subdir.name, count))

    return subdir_counts

# Example usage
# subdir_list = list_subdirectories_with_count('data/CWE_Data')
# markdown_table = "| Subdirectory | Count of Innermost Subdirectories |\n|---------------|-----------------------------------|\n"
# for name, count in subdir_list:
#     markdown_table += f"| {name} | {count} |\n"

# print(markdown_table)


