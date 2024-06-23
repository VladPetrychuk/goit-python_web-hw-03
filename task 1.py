import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

def copy_file(src_path, dest_dir):
    ext = src_path.suffix[1:] 
    target_dir = dest_dir / ext

    target_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy(src_path, target_dir / src_path.name)

def process_directory(src_dir, dest_dir):

    with ThreadPoolExecutor() as executor:
        futures = []

        for root, _, files in os.walk(src_dir):
            for file in files:
                src_path = Path(root) / file
                futures.append(executor.submit(copy_file, src_path, dest_dir))

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                print(f"An error occurred: {exc}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <source_directory> [<destination_directory>]")
        sys.exit(1)

    src_dir = Path(sys.argv[1])
    dest_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("dist")

    if not src_dir.is_dir():
        print(f"Source directory {src_dir} does not exist.")
        sys.exit(1)

    dest_dir.mkdir(parents=True, exist_ok=True)

    process_directory(src_dir, dest_dir)

if __name__ == "__main__":
    main()