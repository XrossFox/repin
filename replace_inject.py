"""Main an only module for this thing
"""
import os
import numbers
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
    """Replaces substrings in the file name of all files in the specified
    directory using REGEX.

    Args:
        path_to_directory (str): Path to directory
        pattern (str): REGEX pattern
        replace_with (str): Substring to replace the pattern
    """
    files = get_files(path_to_directory)
    for file in files:
        rename_file_regex(path_to_file=file, pattern=pattern, replace_with=replace_with)

def delete_with_pattern_regex(path_to_directory: str, pattern: str):
    """Deletes the substring in the file name of all files in the specified
    Directory using REGEX

    Args:
        path_to_directory (str): Path to directory
        pattern (str): Regex pattern
    """
    files = get_files(path_to_directory)
    for file in files:
        rename_file_regex(path_to_file=file, pattern=pattern, replace_with="")

def inject_at_position(path_to_directory: str, position: int, string: str):
    """Injects a string at desired position

    Args:
        path_to_directory (str): Path to directory
        position (int): Position to inject string
        string (str): string
    """
    if not isinstance(position, numbers.Number):
        raise TypeError(f"{position} ain't a number, pal")
    files = get_files(path_to_directory)
    for file in files:
        inject(file, position, string)

def inject(path_to_file: str, position: int, string: str):
    """Injects a string

    Args:
        path_to_file (str): Path to desired file.
        position (int): Position at where to inject string. 0 based.
        string (str): The actual string to inject.
    """
    _, name = os.path.split(path_to_file)
    # must be 0 or positive to work correctly
    if position >= 0:
        name_tmp_1 = name[:position]
        name_tmp_2 = name[position:]
        new_name = name_tmp_1 + string + name_tmp_2
    # for anything else, just default to append at the end
    else:
        new_name = name + string

    rename_file(path_to_file, new_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('path')
    parser.add_argument('-p', "--pattern-replace",
                        help=("Use in conjunction with --replace-with or --delete."
                              " REGEX pattern to look for."),
                        default=None)
    parser.add_argument('-d',
                        '--delete',
                        help=("Use in conjunction with --pattern-replace."
                              " Will delete any matches"),
                        action="store_true")
    parser.add_argument('-r',
                        '--replace-with',
                        help=("Use in conjunction with --pattern-replace."
                              " Will search for a pattern and replace it with"
                              " whatever you put here."),
                        default=None)
    parser.add_argument('-i',
                        '--inject',
                        help=("Use in conjunction with --position, --head, --tail"
                              " (mutually exclusive) and --string. Will inyect"
                              " a specified string at the defined position"),
                        action="store_true")
    parser.add_argument('-n',
                        '--position',
                        help=("The position at where to inyect the string, 0 based."
                              " Exclusive to the right"),
                        default=None,
                        type=int)
    parser.add_argument('-s',
                        '--string',
                        help=("The string to inject."),
                        default=None)
    parser.add_argument('-e',
                        '--head',
                        help=("Place string at the beginning"),
                        action="store_true")
    parser.add_argument('-t',
                        '--tail',
                        help=("Place string at the end"),
                        action="store_true")
    args = parser.parse_args()

    try:
        # --replace-with
        if args.replace_with is not None:
            print("Replace Mode")
            print(f"Replace With: {args.replace_with}")
            if args.pattern_replace is not None:
                print(f"REGEX Pattern: {args.pattern_replace}")
                replace_with_pattern_regex(args.path, args.pattern_replace, args.replace_with)
            else:
                print("--pattern-replace has not been set.")

        # --delete
        elif args.delete is True:
            print("Delete Mode")
            if args.pattern_replace is not None:
                print(f"REGEX Pattern: {args.pattern_replace}")
                delete_with_pattern_regex(args.path, args.pattern_replace)
            else:
                print("--pattern-replace has not been set.")

        # inject
        elif args.inject is True:
            print("Inject Mode")
            if args.string is not None:
                if args.position is not None:
                    # inject at position
                    inject_at_position(args.path, args.position, args.string)
                elif args.head is True:
                    # inject at start
                    inject_at_position(args.path, 0, args.string)
                elif args.tail is True:
                    # inject at end
                    inject_at_position(args.path, -1, args.string)
                else:
                    print("No position specified.")
            else:
                print("String not specified")

        # No option
        else:
            print("Option has not been set.")
    except Exception as e:
        print(e)
