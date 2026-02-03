import argparse
import os
from pathlib import Path

from huggingface_hub import HfApi


def main():
    parser = argparse.ArgumentParser(description="Upload dataset zip to Hugging Face Hub.")
    parser.add_argument(
        "--repo_id",
        default="GemimaOndele/questcrafter-dataset",
        help="Hugging Face dataset repo id (e.g., user/name).",
    )
    parser.add_argument(
        "--file",
        default=r"C:\Users\gemim\OneDrive\Bureau\M1-cours-Data engineer\MSC 1 AI\Semestre 2\Foundations of machine learning and datascience\Project\archive.zip",
        help="Path to archive.zip to upload.",
    )
    parser.add_argument(
        "--commit_message",
        default="Add archive.zip",
        help="Commit message for the upload.",
    )
    parser.add_argument(
        "--token",
        default=None,
        help="Hugging Face token (optional). If omitted, uses HF_TOKEN or cached login.",
    )
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    token = args.token or os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError(
            "No Hugging Face token found. Set HF_TOKEN or pass --token."
        )

    api = HfApi(token=token)
    api.create_repo(
        repo_id=args.repo_id,
        repo_type="dataset",
        exist_ok=True,
    )
    api.upload_file(
        path_or_fileobj=str(file_path),
        path_in_repo=file_path.name,
        repo_id=args.repo_id,
        repo_type="dataset",
        commit_message=args.commit_message,
    )
    print(f"Uploaded {file_path.name} to {args.repo_id}")


if __name__ == "__main__":
    main()
