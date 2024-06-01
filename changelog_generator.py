import os
import sys
import filecmp

def generate_changelog(old_folder, new_folder):
    removed_files = []
    changed_files = []
    added_files = []

    # Compare files and directories recursively
    for root, dirs, files in os.walk(old_folder):
        for file in files:
            old_file_path = os.path.join(root, file)
            new_file_path = os.path.join(new_folder, os.path.relpath(old_file_path, old_folder))

            if not os.path.exists(new_file_path):
                removed_files.append(os.path.relpath(old_file_path, old_folder))
            elif not filecmp.cmp(old_file_path, new_file_path, shallow=False):
                changed_files.append(os.path.relpath(old_file_path, old_folder))

    for root, dirs, files in os.walk(new_folder):
        for file in files:
            new_file_path = os.path.join(root, file)
            old_file_path = os.path.join(old_folder, os.path.relpath(new_file_path, new_folder))

            if not os.path.exists(old_file_path):
                added_files.append(os.path.relpath(new_file_path, new_folder))

    # Write the changelog to a file
    with open("changelog.txt", "w") as changelog_file:
        if removed_files:
            changelog_file.write("removed:\n")
            for file in removed_files:
                changelog_file.write(f"    {file}\n")

        if changed_files:
            changelog_file.write("changed:\n")
            for file in changed_files:
                changelog_file.write(f"    {file}\n")

        if added_files:
            changelog_file.write("added:\n")
            for file in added_files:
                changelog_file.write(f"    {file}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python changelog_generator.py <old_folder> <new_folder>")
        sys.exit(1)

    old_folder = sys.argv[1]
    new_folder = sys.argv[2]

    if not os.path.exists(old_folder) or not os.path.isdir(old_folder):
        print(f"Error: {old_folder} does not exist or is not a directory.")
        sys.exit(1)

    if not os.path.exists(new_folder) or not os.path.isdir(new_folder):
        print(f"Error: {new_folder} does not exist or is not a directory.")
        sys.exit(1)

    generate_changelog(old_folder, new_folder)
