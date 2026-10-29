import csv
import json
from pathlib import Path


INPUT_FILE = Path("data/folio-train.txt")
OUTPUT_FILE = Path("training/nyaya_folio_dataset.json")


def create_record(row):
    premises = row["premises"]
    premises_fol = row["premises-FOL"]
    conclusion = row["conclusion"]
    label = row["label"]

    return {
        "instruction": (
            "Solve the logical problem using the six Nyaya stages: "
            "Samshaya, Pramana, Pancha Avayava, Tarka, "
            "Hetvabhasa, and Nirnaya."
        ),

        "input": {
            "premises": premises,
            "premises_fol": premises_fol,
            "question": conclusion
        },

        "output": {
            "samshaya": (
                "Determine whether the stated conclusion follows "
                "from the given premises."
            ),

            "pramana": (
                "Use the supplied premises and their formal logical "
                "representation as the evidence for reasoning."
            ),

            "pancha_avayava": {
                "pratijna": (
                    "State the claim that must be evaluated."
                ),

                "hetu": (
                    "Identify the relevant facts or rules in the premises "
                    "that support or contradict the claim."
                ),

                "udaharana": (
                    "Identify the general logical relationship expressed "
                    "by the premises."
                ),

                "upanaya": (
                    "Apply the relevant premises to the entities and "
                    "properties in the claim."
                ),

                "nigamana": (
                    "Derive the result from the applied premises."
                )
            },

            "tarka": (
                "Consider whether assuming the opposite of the claim "
                "would be consistent with the premises."
            ),

            "hetvabhasa": (
                "Check whether the reasoning contains an unsupported, "
                "contradictory, or invalid inference."
            ),

            "nirnaya": (
                "State the logical determination reached from the premises."
            ),

            "label": label
        }
    }


def main():
    records = []

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter="\t")

        for row in reader:
            records.append(create_record(row))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            records,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(f"Created {len(records)} Nyaya-formatted examples.")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()