#########
# FileMap
#########

# Maps from a string key to a file
# Implemented as an an array of files and directories
# Example:
# Key = "dog"
# Filestructure:
# a/
#   p/
#     p
# d/
#   o/
#     g

# Written by ChatGPT

import os
import chardet
from pathlib import Path


class FileMap:
    def __init__(self):
        self._root_dir = {}

    def add_file(self, key, file_path):
        self._root_dir[key] = file_path

    def get_file(self, key):
        return self._root_dir.get(key, None)

    def to_file_structure(self, base_directory):
        for key, value in self._root_dir.items():
            file_path = Path(base_directory) / value
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w') as file:
                file.write(str(key))

    def from_file_structure(self, base_directory):
        for file_path in Path(base_directory).rglob('*'):
            if file_path.is_file():
                encoding = self._detect_encoding(file_path)
                with open(file_path, 'r', encoding=encoding) as file:
                    key = file.read()
                    self._root_dir[key] = str(file_path.relative_to(base_directory))

    def _detect_encoding(self, file_path):
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            return result['encoding']

    @property
    def root_dir(self):
        return self._root_dir.copy()


if __name__ == "__main__":
    file_map = FileMap()

    # Adding files to the file map
    file_map.add_file("dog", "a/p/p.txt")
    file_map.add_file("cat", "d/o/g.txt")

    # Convert file map to file structure
    current_directory = Path.cwd()

    # Set DB path
    db_path = current_directory / "db"
    file_map.to_file_structure(db_path)

    # Display the file map
    print("File Map:")
    for key, value in file_map.root_dir.items():
        print(f"Key: {key}, File Path: {value}")

    # Create a new FileMap object
    new_file_map = FileMap()

    # Populate the file map from the file structure
    new_file_map.from_file_structure(db_path)

    # Display the populated file map
    print("\nPopulated File Map:")
    for key, value in new_file_map.root_dir.items():
        print(f"Key: {key}, File Path: {value}")
