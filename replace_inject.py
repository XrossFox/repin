"""Main an only module for this thing"""

import os
import re
import argparse

DRY_RUN = False


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
    if not DRY_RUN:
        os.rename(path_to_file, new_path)
    print(f"{path_to_file} Renamed to -> {new_name}")


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


def replace_with_sequence(
    path_to_directory: str, start: int, step: int, stop: int, pattern: str
):
    """Delivers a numeric sequence at the desired position of the name of files in a directory.

    Args:
        path_to_directory (str): Path to directory.
        position (int): Position of the squence in the name of the file.
        start (int): Starting number of the sequence.
        step (int): Amount to increment to the sequence on each iteration
        stop (int): Stopping number of the sequence (exclusive to the right).
    """
    if start < 0 or step < 0 or stop < 0:
        print(
            f"Invalid value for start = {start}/step = {step}/stop = {stop}: cannot be less than 0"
        )
        return

    files = get_files(path_to_directory)
    if stop < len(files):
        print(
            "Numeric sequence is smaller than count of files in directory. Cannot proceed further."
        )
        return

    sequence = iter(range(start, stop, step))

    for file in files:
        current = next(sequence)
        rename_file_regex(path_to_file=file, pattern=pattern, replace_with=str(current))


def sequence_at_position(
    path_to_directory: str, position: int, start: int, step: int, stop: int
):
    """Delivers a numeric sequence at the desired position of the name of files in a directory.

    Args:
        path_to_directory (str): Path to directory.
        position (int): Position of the squence in the name of the file.
        start (int): Starting number of the sequence.
        step (int): Amount to increment to the sequence on each iteration
        stop (int): Stopping number of the sequence (exclusive to the right).
    """
    if start < 0 or step < 0 or stop < 0:
        print(
            f"Invalid value for start = {start}/step = {step}/stop = {stop}: cannot be less than 0"
        )
        return

    files = get_files(path_to_directory)
    if stop < len(files):
        print(
            "Numeric sequence is smaller than count of files in directory. Cannot proceed further."
        )
        return

    sequence = iter(range(start, stop, step))

    for file in files:
        current = next(sequence)
        inject(file, position, str(current))


def inject_at_position(path_to_directory: str, position: int, string: str):
    """Injects a string at desired position

    Args:
        path_to_directory (str): Path to directory
        position (int): Position to inject string
        string (str): string
    """
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

    parser.add_argument("path")
    parser.add_argument(
        "-p",
        "--pattern",
        help=(
            "Use in conjunction with --replace-with or --delete."
            " REGEX pattern to look for."
        ),
        default=None,
    )
    parser.add_argument(
        "-d",
        "--delete",
        help=("Use in conjunction with --pattern." " Will delete any matches"),
        action="store_true",
    )
    parser.add_argument(
        "-j",
        "--replace-with-sequence",
        help=(
            "Use in conjunction with --pattern, --start, --step, --stop."
            " Will search for a pattern and replace it with"
            " a number in a sequence."
        ),
        action="store_true",
    )
    parser.add_argument(
        "-r",
        "--replace-with",
        help=(
            "Use in conjunction with --pattern."
            " Will search for a pattern and replace it with"
            " whatever you put here."
        ),
        default=None,
    )
    parser.add_argument(
        "-i",
        "--inject",
        help=(
            "Use in conjunction with --position, --head, --tail"
            " (mutually exclusive) and --string. Will inyect"
            " the specified string at the defined position"
        ),
        default=None,
    )
    parser.add_argument(
        "-q",
        "--inject-sequence",
        help=(
            "Use in conjunction with --position, --head, --tail"
            " (mutually exclusive), --string, --start, --step, --stop."
            " Will inyect"
            " a numeric sequence at the desired position."
        ),
        action="store_true",
    )
    parser.add_argument(
        "-n",
        "--position",
        help=(
            "The position at where to inyect the string, 0 based."
            " Exclusive to the right"
        ),
        default=None,
        type=int,
    )
    parser.add_argument(
        "-u",
        "--start",
        help=(
            "The starting point of the numeric sequence."
            " Cannot be less than 0, or less than the count of files"
        ),
        default=0,
        type=int,
    )
    parser.add_argument(
        "-v",
        "--step",
        help=("The value at what number the sequence increments with each iteration"),
        default=1,
        type=int,
    )
    parser.add_argument(
        "-x",
        "--stop",
        help=(
            "The value at what pace the sequence increments with each iteration,"
            " exclusive to ther right. Cannot be less than 0, or less than start."
        ),
        default=0,
        type=int,
    )
    parser.add_argument(
        "-e", "--head", help=("Place string at the beginning"), action="store_true"
    )
    parser.add_argument(
        "-t", "--tail", help=("Place string at the end"), action="store_true"
    )
    parser.add_argument(
        "-a",
        "--dry-run",
        help=("Dry run: doesn`t actually rename the files"),
        action="store_true",
    )
    args = parser.parse_args()

    try:
        # --dry-run
        if args.dry_run:
            DRY_RUN = True

        # --replace-with
        if args.replace_with is not None:
            print("Replace Mode")
            print(f"Replace With: {args.replace_with}")
            if args.pattern is not None:
                print(f"REGEX Pattern: {args.pattern}")
                replace_with_pattern_regex(
                    args.path, args.pattern, args.replace_with
                )
            else:
                print("--pattern has not been set.")

        # --replace-with-sequence
        elif args.replace_with_sequence:
            print("Replace with sequence Mode")
            if args.start > 0 and args.stop > args.start:
                if args.pattern is not None:
                    print(f"REGEX Pattern: {args.pattern}")
                    replace_with_sequence(
                        args.path, args.start, args.step, args.stop, args.pattern
                    )
                else:
                    print("No pattern specified.")
            else:
                print(
                    f"Start is 0, or less than stop. start:{args.start}, stop:{args.stop}"
                )

        # --delete
        elif args.delete is True:
            print("Delete Mode")
            if args.pattern is not None:
                print(f"REGEX Pattern: {args.pattern}")
                delete_with_pattern_regex(args.path, args.pattern)
            else:
                print("--pattern has not been set.")

        # --inject
        elif args.inject is not None:
            print("Inject Mode")
            if args.position is not None:
                # inject at position
                inject_at_position(args.path, args.position, args.inject)
            elif args.head is True:
                # inject at start
                inject_at_position(args.path, 0, args.inject)
            elif args.tail is True:
                # inject at end
                inject_at_position(args.path, -1, args.inject)
            else:
                print("No position specified.")

        # --inject-sequence
        elif args.inject_sequence is True:
            print("Inject Sequence Mode")
            if args.start > 0 and args.stop > args.start:
                if args.position is not None:
                    # inject at position
                    sequence_at_position(
                        args.path,
                        args.position,
                        args.start,
                        args.step,
                        args.stop,
                    )
                elif args.head is True:
                    # inject at start
                    sequence_at_position(args.path, 0, args.start, args.step, args.stop)
                elif args.tail is True:
                    # inject at end
                    sequence_at_position(
                        args.path, -1, args.start, args.step, args.stop
                    )
                else:
                    print("No position specified.")
            else:
                print(
                    f"Start is 0, or less than stop. start:{args.start}, stop:{args.stop}"
                )

        # No option
        else:
            print("Option has not been set.")
    except Exception as e:
        print(e)
