import os
import datetime
import shutil

def create_backup():
    # Create a backup directory with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_{timestamp}"
    os.makedirs(backup_dir)

    # Copy all code files
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".py", ".html", ".css", ".js")):
                src_path = os.path.join(root, file)
                dst_path = os.path.join(backup_dir, os.path.relpath(src_path, "."))
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)

    # Create a file for environment variables (without sensitive information)
    with open(os.path.join(backup_dir, "environment_variables.txt"), "w") as f:
        for key, value in os.environ.items():
            if not key.startswith(("OPENAI_API_KEY", "PG", "DATABASE_URL")):
                f.write(f"{key}={value}\n")

    print(f"Backup created in '{backup_dir}' directory.")

if __name__ == "__main__":
    create_backup()
