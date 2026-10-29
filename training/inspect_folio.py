import csv
from pathlib import Path
from collections import Counter


DATA_FILE = Path("data/folio-train.txt")


def main():
    labels = Counter()
    total = 0

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(
            file,
            delimiter="\t"
        )

        for row in reader:
            total += 1
            labels[row["label"]] += 1

    print("FOLIO dataset inspection")
    print("------------------------")
    print(f"Total examples: {total}")
    print()
    print("Labels:")

    for label, count in labels.items():
        print(f"  {label}: {count}")


if __name__ == "__main__":
    main()