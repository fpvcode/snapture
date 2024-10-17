"""
Module:         snapture.py
Description:    A tool to snapshot file structures into a single file and restore it.
Author:         Andrii Burkatskyi aka underr
Year:           2024
Version:        1.0.0.241017
License:        MIT License
Email:          fpvcode@gmail.com
"""

import os
import hashlib
import sys
import argparse


def hash(file_path):
    """Compute the given file SHA-256."""

    sha256 = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


def mksnap(input_dir, snap_file):
    """Create file structure snapshot into a single file"""

    base_dir = os.path.abspath(input_dir)

    try:
        with open(snap_file, 'wb') as f:
            for root, dirs, files in os.walk(base_dir):
                relative_root = os.path.relpath(root, base_dir)

                if relative_root == '.':
                    relative_root = ''  # Clear './'

                # Store information about directories
                for dir_name in dirs:
                    dir_path = os.path.join(relative_root, dir_name)
                    dir_mode = oct(os.stat(os.path.join(root, dir_name)).st_mode)[-3:] if os.name != 'nt' else '777'
                    dir_info = f"{dir_path}|d|{dir_mode}|0|\n"

                    f.write(dir_info.encode('utf-8'))
                    print(dir_path)

                # Store information about files
                for file_name in files:
                    abs_file_path = os.path.join(root, file_name)

                    # Skip snap-file itself
                    if os.path.abspath(abs_file_path) == os.path.abspath(snap_file):
                        continue

                    # Skip scrypt itself
                    if os.path.abspath(abs_file_path) == os.path.abspath(__file__):
                        continue

                    file_path = os.path.join(relative_root, file_name)
                    file_size = os.path.getsize(abs_file_path)
                    file_permissions = oct(os.stat(abs_file_path).st_mode)[-3:] if os.name != 'nt' else '666'
                    file_hash = hash(abs_file_path)

                    file_info = f"{file_path}|f|{file_permissions}|{file_size}|{file_hash}\n"
                    f.write(file_info.encode('utf-8'))

                    # Write file content
                    with open(abs_file_path, 'rb') as file_content:
                        f.write(file_content.read())

                    print(file_path)

                    # New line for a nicer structure
                    f.write(b'\n')

        print(f"\n{os.path.getsize(os.path.abspath(snap_file))}")
    except Exception as e:
        print(f"Error while snap file structure: {e}")


def unsnap(snap_file, output_dir, strict_mode=True):
    """Restore file structure from snapshot file"""

    try:
        with open(snap_file, 'rb') as f:
            while True:
                line = f.readline().decode('utf-8').strip()

                if not line:
                    break

                # Parse metadata
                name, type_, permissions, size, file_hash = line.split('|')
                size = int(size)
                new_path = os.path.join(output_dir, name)

                if type_ == 'd':
                    os.makedirs(new_path, exist_ok=True)
                    print(new_path + '/')

                    if os.name != 'nt':
                        os.chmod(new_path, int(permissions, 8))
                elif type_ == 'f':
                    # Restore file content
                    with open(new_path, 'wb') as file_out:
                        file_out.write(f.read(size))

                    if hash(new_path) != file_hash:
                        print(f"{new_path} - Hash mismatch!")
                        os.remove(new_path)

                        # If strict mode is enabled, exit on hash mismatch
                        if strict_mode:
                            sys.exit(1)
                    else:
                        print(new_path)

                        if os.name != 'nt':
                            os.chmod(new_path, int(permissions, 8))

                # Skip any empty lines between files
                while True:
                    pos = f.tell()  # Save current position
                    next_line = f.readline().decode('utf-8').strip()

                    # Check whether the file end has been reached
                    if not next_line:  # Empty line
                        if f.tell() == os.fstat(f.fileno()).st_size:  # The end of the file
                            break
                    else:
                        f.seek(pos)  # Back to metadata
                        break
    except Exception as e:
        print(f"Error while unsnap file structure: {e}")


def list_snap(snap_file):
    """List directories and files stored in snap-structure"""

    try:
        with open(snap_file, 'rb') as f:
            while True:
                line = f.readline().decode('utf-8').strip()

                if not line:
                    break

                # Parse metadata
                name, type_, permissions, size, file_hash = line.split('|')
                size = int(size)

                # Print out the file or directory
                print(f"{name + '/' if type_ == 'd' else name + ' - ' + str(round(size / 1024, 2)) + 'kB'}")

                # Skip binary data of the file
                if type_ == 'f':
                    f.seek(f.tell() + size)  # Skip the file content

                # Skip any empty lines between files
                while True:
                    pos = f.tell()  # Save current position
                    next_line = f.readline().decode('utf-8').strip()

                    # Check whether the file end has been reached
                    if not next_line:  # Empty line
                        if f.tell() == os.fstat(f.fileno()).st_size:  # The end of the file
                            break
                    else:
                        f.seek(pos)  # Back to metadata
                        break

    except Exception as e:
        print(f"Error while listing snap file structure: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Snapture: A tool to save file structures into a single file and restore it."
    )
    parser.add_argument('-m', action='store_true', help="Create a snap-structure in a file")
    parser.add_argument('-u', action='store_true', help="Restore from a snap-structure")
    parser.add_argument('-s', action='store_true', help="Disable strict mode (continue on file hash mismatch)")
    parser.add_argument('-l', metavar="snap_file", type=str, help="List files and directories stored in snap file")
    parser.add_argument('-d', metavar="directory", type=str, required=False, help="Path to the directory")
    parser.add_argument('-f', metavar="snap_file", type=str, required=False, help="Path to the snap file")
    args = parser.parse_args()

    if args.l:
        list_snap(args.l)
        sys.exit(0)

    if not args.m and not args.u:
        parser.print_help()
        sys.exit(1)

    if args.m:
        if not args.d or not args.f:
            print("Error: Both -d (directory) and -f (file) parameters are required for snap creation.")
            sys.exit(1)

        mksnap(args.d, args.f)
    elif args.u:
        if not args.d or not args.f:
            print("Error: Both -d (directory) and -f (file) parameters are required for snap restoration.")
            sys.exit(1)

        unsnap(args.f, args.d, strict_mode=not args.s)


if __name__ == "__main__":
    main()
