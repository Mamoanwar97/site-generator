import os
import shutil

def copy_directory_contents(src, dst):
    """
    Recursively copies all contents from source directory to destination directory.
    
    Args:
        src: Source directory path
        dst: Destination directory path
    """
    # First, clean the destination directory
    if os.path.exists(dst):
        print(f"Deleting destination directory: {dst}")
        shutil.rmtree(dst)
    
    # Create the destination directory
    print(f"Creating destination directory: {dst}")
    os.mkdir(dst)
    
    # Recursively copy contents
    _copy_recursive(src, dst)


def _copy_recursive(src, dst):
    """
    Helper function to recursively copy directory contents.
    
    Args:
        src: Source directory path
        dst: Destination directory path
    """
    # List all items in the source directory
    items = os.listdir(src)
    
    for item in items:
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isfile(src_path):
            # Copy file
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            # It's a directory, create it and recurse
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            _copy_recursive(src_path, dst_path)



