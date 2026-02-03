import os
import subprocess
import sys


def get_staged_files():
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=AM"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main():
    max_mb = float(os.environ.get("MAX_FILE_SIZE_MB", "100"))
    max_bytes = int(max_mb * 1024 * 1024)

    oversized = []
    for path in get_staged_files():
        if not os.path.isfile(path):
            continue
        try:
            size = os.path.getsize(path)
        except OSError:
            continue
        if size > max_bytes:
            oversized.append((path, size))

    if oversized:
        print("ERROR: fichiers trop volumineux dans le commit.")
        print(f"Limite: {max_mb:.0f} MB")
        for path, size in oversized:
            size_mb = size / (1024 * 1024)
            print(f"- {path} ({size_mb:.2f} MB)")
        print("Supprime-les du commit ou utilise Git LFS si nécessaire.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
