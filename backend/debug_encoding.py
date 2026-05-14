
import sys
import os
import pkgutil
import importlib

# Add backend to path
sys.path.append(os.getcwd())

def test_imports():
    print("Starting import check...")
    
    # Walk through app directory
    root_path = os.path.join(os.getcwd(), "app")
    
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                module_path = os.path.relpath(file_path, os.getcwd()).replace(os.sep, ".")[:-3]
                
                try:
                    print(f"Importing {module_path}...", end="", flush=True)
                    # We just try to open and read it first to check encoding
                    with open(file_path, "r", encoding="utf-8") as f:
                        f.read()
                    print(" OK (encoding)", end="", flush=True)
                    
                    # Then try to import
                    # importlib.import_module(module_path)
                    # print(" OK (import)")
                    print("")
                except UnicodeDecodeError:
                    print(f" FAIL: UnicodeDecodeError in {file_path}")
                except Exception as e:
                    print(f" FAIL: {e}")

if __name__ == "__main__":
    test_imports()
