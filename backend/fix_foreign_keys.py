
import os

def fix_foreign_keys():
    print("Fixing foreign keys...")
    root_path = os.path.join(os.getcwd(), "app", "modules")
    
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file == "models.py":
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    if 'ForeignKey("user.id")' in content:
                        print(f"Fixing {file_path}...")
                        new_content = content.replace('ForeignKey("user.id")', 'ForeignKey("users.id")')
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    fix_foreign_keys()
