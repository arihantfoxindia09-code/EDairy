import os
import tempfile
from filelock import FileLock
import shutil

class FileWriter:
    def __init__(self):
        self.file_path = 'diary_entry.txt'
        self.lock = FileLock(f"{self.file_path}.lock")  # Create a lock file for concurrency

    def get_content(self):
        """Read the content of the file."""
        try:
            with self.lock:  # Acquire the lock to ensure thread safety
                if os.path.exists(self.file_path):
                    with open(self.file_path, 'r', encoding='utf-8') as file:
                        return file.read()
                else:
                    return ""
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""

    def clear_content(self):
        """Clear the content of the file."""
        try:
            with self.lock:  # Acquire the lock
                open(self.file_path, 'w').close()  # Clear the file's content by opening it in write mode
                print(f"File content cleared: {self.file_path}")
        except Exception as e:
            print(f"Error clearing file content: {e}")

    def overwrite_content(self, content):
        """Overwrite the file content in an efficient and atomic manner."""
        try:
            with self.lock:  # Acquire the lock to ensure thread safety
                # Use a temporary file to avoid partial writes in case of failure
                temp_file_path = tempfile.mktemp()  # Create a temporary file

                with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
                    temp_file.write(content)  # Write the new content to the temp file

                # Rename the temporary file to the target file atomically (replace original file)
                os.replace(temp_file_path, self.file_path)  # Atomic operation for file replacement

                print(f"File content overwritten successfully: {self.file_path}")
        except Exception as e:
            print(f"Error overwriting file content: {e}")

    def append_content(self, content):
        """Append content to the file efficiently."""
        try:
            with self.lock:  # Acquire the lock to ensure thread safety
                with open(self.file_path, 'a', encoding='utf-8') as file:
                    file.write(content)  # Append the content to the file
                print(f"Content appended to file: {self.file_path}")
        except Exception as e:
            print(f"Error appending content to file: {e}")



# Initialize the FileWriter instance for a specific file path
file_writer = FileWriter()

# Overwrite the file content
file_writer.overwrite_content("This is a new diary entry.\nEverything is going well!")

# Append to the file
file_writer.append_content("\nAdditional entry: Things are looking great!")

# Get the file content
content = file_writer.get_content()
print(content)  # Output the content of the file

# Clear the content
file_writer.clear_content()
