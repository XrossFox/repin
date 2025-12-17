"""Main an only module for this thing
"""
import os
import re
import argparse

def get_files(path_to_directory: str) -> list:
    """Returns all files in a directory. Directories will be ommitted.

    Args:
        path (str): Path to directory

    Returns:
        List: A list of files paths.
    """
    files = []
    for file in os.listdir(path_to_directory):
        full_path = os.path.join(path_to_directory, file)
        if os.path.isfile(full_path):
            files.append(full_path)
    return files

def rename_file(path_to_file: str, new_name: str):
    """Renames a file

    Args:
        path_to_file (str): Path to file
        new_name (str): New name for the file
    """
    path_only, _ = os.path.split(path_to_file)
    new_path = os.path.join(path_only, new_name)
    os.rename(path_to_file, new_path)

def rename_file_regex(path_to_file: str, pattern: str, replace_with: str):
    """Renames a file and replaces the substring according with the desired regex pattern.

    Args:
        path_to_file (str): Path to the file to rename
        pattern (str): Regex Pattern
        replace_with (str): Substring to replace pattern with
    """
    _, filename = os.path.split(path_to_file)
    new_filename = re.sub(pattern=pattern, repl=replace_with, string=filename)

    rename_file(path_to_file=path_to_file, new_name=new_filename)

def replace_with_pattern_regex(path_to_directory: str, pattern: str, replace_with: str):
    """Replaces substrings in the file name of all filles in the specified
    directory using REGEX.

    Args:
        path_to_directory (str): Path to directory
        pattern (str): REGEX pattern
        replace_with (str): Substring to replace the pattern
    """
    files = get_files(path_to_directory)
    for file in files:
        rename_file_regex(path_to_file=file, pattern=pattern, replace_with=replace_with)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('path')
    parser.add_argument('-p', "--pattern-replace",
                        help=("Use in conjunction with --replace-with."
                              " REGEX pattern to look for."),
                        default=None)
    parser.add_argument('-r',
                        '--replace-with',
                        help=("Use in conjunction with --pattern-replace."
                              " Will search for a pattern and replace it with"
                              " whatever you put here."),
                        default=None)
    args = parser.parse_args()

    try:
        if args.replace_with is not None:
            print(f"Replace With: {args.replace_with}")
            if args.pattern_replace is not None:
                print(f"REGEX Pattern: {args.pattern_replace}")
                replace_with_pattern_regex(args.path, args.pattern_replace, args.replace_with)
            else:
                print("--pattern-replace has not been set.")
        else:
            print("--replace-with has not been set.")
    except Exception as e:
        print(e)
