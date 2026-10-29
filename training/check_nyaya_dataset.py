import json
from pathlib import Path
from collections import Counter


INPUT_FILE = Path("training/nyaya_folio_dataset.json")


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    labels = Counter(
        record["output"]["label"]
        for record in records
    )

    print("Nyaya dataset check")
    print("--------------------")
    print(f"Total examples: {len(records)}")
    print()

    print("Labels:")
    for label, count in labels.items():
        print(f"  {label}: {count}")

    print()
    print("Checking required fields...")

    required_output = [
        "samshaya",
        "pramana",
        "pancha_avayava",
        "tarka",
        "hetvabhasa",
        "nirnaya",
        "label"
    ]

    required_pancha = [
        "pratijna",
        "hetu",
        "udaharana",
        "upanaya",
        "nigamana"
    ]

    errors = 0

    for index, record in enumerate(records):

        for field in ["instruction", "input", "output"]:
            if field not in record:
                print(f"Missing '{field}' in example {index}")
                errors += 1

        output = record["output"]

        for field in required_output:
            if field not in output:
                print(f"Missing '{field}' in example {index}")
                errors += 1

        pancha = output.get("pancha_avayava", {})

        for field in required_pancha:
            if field not in pancha:
                print(
                    f"Missing Pancha Avayava '{field}' "
                    f"in example {index}"
                )
                errors += 1

    print()

    if errors == 0:
        print("Dataset structure is valid.")
    else:
        print(f"Found {errors} structural errors.")


if __name__ == "__main__":
    main()