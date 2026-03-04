import argparse
import csv
from pathlib import Path


def sniff_dialect(path: Path):
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        sample = handle.read(10000)
    try:
        return csv.Sniffer().sniff(sample)
    except csv.Error:
        return csv.excel


def sample_csv(path: Path, output_path: Path, max_rows: int) -> int:
    dialect = sniff_dialect(path)
    if not getattr(dialect, "escapechar", None):
        dialect.escapechar = "\\"
    if not getattr(dialect, "doublequote", None):
        dialect.doublequote = True
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.reader(handle, dialect)
        try:
            header = next(reader)
        except StopIteration:
            return 0

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8", newline="") as out:
            writer = csv.writer(out, dialect)
            writer.writerow(header)

            count = 0
            for row in reader:
                writer.writerow(row)
                count += 1
                if count >= max_rows:
                    break
    return count


def main():
    parser = argparse.ArgumentParser(
        description="Create small CSV samples for GitHub commits."
    )
    parser.add_argument(
        "--input_dir",
        default="dataset",
        help="Folder that contains full CSV files.",
    )
    parser.add_argument(
        "--output_dir",
        default="dataset/sample",
        help="Folder to write smaller CSV files.",
    )
    parser.add_argument(
        "--max_rows",
        type=int,
        default=1000,
        help="Maximum number of data rows per file (header not counted).",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        raise SystemExit(f"Input folder not found: {input_dir}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(input_dir.glob("*.csv"))
    if not csv_files:
        raise SystemExit(f"No CSV files found in: {input_dir}")

    for path in csv_files:
        output_path = output_dir / path.name
        written = sample_csv(path, output_path, args.max_rows)
        print(f"{path.name}: {written} rows -> {output_path}")


if __name__ == "__main__":
    main()
