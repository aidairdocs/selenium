#!/usr/bin/env python3
"""
generate_sitemap.py

Recursively scans the current project's folder structure
and writes a hierarchical listing to 'readme.md' (overwrites it).

Example usage:
    python generate_sitemap.py

Result:
    A readme.md file with a tree-like structure:

    .
    ├── folder1
    │   ├── subfile1.py
    │   └── subfile2.py
    ├── folder2
    │   └── subfolder
    │       └── fileA.py
    └── fileB.py
"""

import os

def generate_sitemap(root_dir, indent="", is_last=True, output_lines=None):
    """
    Recursively walks 'root_dir' and appends a tree-like listing
    of directories/files to 'output_lines'.

    :param root_dir: str path to start scanning
    :param indent: str used to control the tree branch visuals
    :param is_last: bool indicating whether this item is the last in its level
    :param output_lines: list of lines to collect the output
    """
    if output_lines is None:
        output_lines = []

    # Prepare the short name (relative to parent)
    base_name = os.path.basename(os.path.normpath(root_dir))

    # If this is the top-level call, we show base_name as "."
    display_name = base_name if indent else "."

    # For top-level folder, no prefix. Otherwise add branch prefix.
    branch_str = indent + ("└── " if is_last else "├── ")
    output_lines.append(f"{branch_str}{display_name}")

    # For sub items, compute new indent
    new_indent = indent + ("    " if is_last else "│   ")

    try:
        # Gather children
        items = os.listdir(root_dir)
    except PermissionError:
        # If we can't access this dir, skip
        return output_lines

    # Filter out hidden/system items if desired
    items = [i for i in items if not i.startswith('.')]

    # Separate dirs and files
    dirs = []
    files = []
    for item in sorted(items, key=str.lower):
        full_path = os.path.join(root_dir, item)
        if os.path.isdir(full_path):
            dirs.append(item)
        else:
            files.append(item)

    # Build up a combined list to process in order: all dirs then all files
    combined = dirs + files

    for idx, item in enumerate(combined):
        full_path = os.path.join(root_dir, item)
        # Determine if it's last
        child_is_last = (idx == len(combined) - 1)
        if os.path.isdir(full_path):
            # Recurse
            generate_sitemap(full_path, new_indent, child_is_last, output_lines)
        else:
            # It's a file
            file_branch_str = new_indent + ("└── " if child_is_last else "├── ")
            output_lines.append(f"{file_branch_str}{item}")

    return output_lines

def main():
    root_dir = os.getcwd()  # current directory
    readme_path = os.path.join(root_dir, "readme.md")

    # Generate the sitemap lines
    lines = generate_sitemap(root_dir)

    # Write them to readme.md
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# Project Folder Structure\n\n")
        f.write("\n".join(lines))
        f.write("\n")

    print(f"[INFO] Sitemap written to {readme_path}")

if __name__ == "__main__":
    main()
