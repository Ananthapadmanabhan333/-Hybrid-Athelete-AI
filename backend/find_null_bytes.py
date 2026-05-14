
import sys
import os

def check_null_bytes():
    print("Checking for null bytes...")
    root_path = os.path.join(os.getcwd(), "app")
    
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as f:
                        content = f.read()
                        if b'\x00' in content:
                            print(f"FOUND NULL BYTES: {file_path}")
                except Exception as e:
                    print(f"Error checking {file_path}: {e}")

if __name__ == "__main__":
    check_null_bytes()
