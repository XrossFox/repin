import os
import argparse

def get_files(path):
    files = []
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path):
            files.append(file)
    return files

def rename_file(path, new_name):
    path_only, _ = os.path.split(path)
    new_path = os.path.join(path_only, new_name)
    os.rename(path, new_path)

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
    # files = get_files(args.path)
    # print(files)
    rename_file(args.path, args.r__replace_with)