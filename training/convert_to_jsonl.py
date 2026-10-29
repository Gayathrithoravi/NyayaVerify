import json
from pathlib import Path


INPUT_FILE = Path("training/nyaya_folio_dataset.json")
OUTPUT_FILE = Path("training/nyaya_folio_train.jsonl")


def format_record(record):
    input_data = record["input"]
    output = record["output"]

    return {
        "text": (
            "### Instruction\n"
            f"{record['instruction']}\n\n"
            "### Input\n"
            f"Premises:\n{input_data['premises']}\n\n"
            f"Formal premises:\n{input_data['premises_fol']}\n\n"
            f"Question:\n{input_data['question']}\n\n"
            "### Output\n"
            f"Samshaya: {output['samshaya']}\n\n"
            f"Pramana: {output['pramana']}\n\n"
            "Pancha Avayava:\n"
            f"Pratijna: {output['pancha_avayava']['pratijna']}\n"
            f"Hetu: {output['pancha_avayava']['hetu']}\n"
            f"Udaharana: {output['pancha_avayava']['udaharana']}\n"
            f"Upanaya: {output['pancha_avayava']['upanaya']}\n"
            f"Nigamana: {output['pancha_avayava']['nigamana']}\n\n"
            f"Tarka: {output['tarka']}\n\n"
            f"Hetvabhasa: {output['hetvabhasa']}\n\n"
            f"Nirnaya: {output['nirnaya']}\n"
        )
    }


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        for record in records:
            formatted = format_record(record)
            file.write(
                json.dumps(
                    formatted,
                    ensure_ascii=False
                ) + "\n"
            )

    print(f"Converted {len(records)} examples.")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()