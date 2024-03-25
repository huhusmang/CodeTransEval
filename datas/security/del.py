from pathlib import Path
import shutil


def is_empty_file(file_path):
    """Check if a file is empty using pathlib."""
    return file_path.stat().st_size == 0

def should_delete_subdir(subdir):
    """Check if a subdir should be deleted based on the files it contains, using pathlib."""
    required_files = ['vul.py', 'sec.py', 'source']
    return all(is_empty_file(subdir / f) for f in required_files)

def delete_empty_directories(parent_dir):
    """Delete empty directories based on specific rules using pathlib."""
    parent_path = Path(parent_dir)
    for root_dir in parent_path.iterdir():
        if root_dir.is_dir():  # Only process directories
            subdirs = [root_dir / str(i) for i in range(1, 6)]
            empty_subdirs = [subdir for subdir in subdirs if subdir.exists() and should_delete_subdir(subdir)]

            if len(empty_subdirs) == 5:
                # Delete the parent directory if all subdirectories are empty
                # for subdir in subdirs:
                #     if subdir.exists():  # Additional check for safety
                #         shutil.rmtree(subdir)
                # root_dir.rmdir()  # Remove the root directory
                shutil.rmtree(root_dir)
            elif empty_subdirs:
                # Only delete empty subdirectories
                for subdir in empty_subdirs:
                    shutil.rmtree(subdir)

# Example usage (replace 'path_to_parent_dir' with the actual path)
delete_empty_directories('data/CWE_Data')
