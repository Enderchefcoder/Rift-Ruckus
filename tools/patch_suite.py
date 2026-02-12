import sys
import os

def apply_patch(filename, search, replace):
    if not os.path.exists(filename):
        return
    with open(filename, 'r') as f:
        content = f.read()
    if search in content:
        new_content = content.replace(search, replace, 1)
        with open(filename, 'w') as f:
            f.write(new_content)
        print(f"Applied patch to {filename}")
    else:
        print(f"Search string not found in {filename}")

# This script can be expanded with the logic from the previous separate files if needed for re-application.
if __name__ == "__main__":
    print("Patch suite initialized. Use functions to apply specific changes.")
