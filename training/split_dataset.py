import json
import random
from pathlib import Path


INPUT_FILE = Path("training/nyaya_folio_dataset.json")

TRAIN_FILE = Path("training/nyaya_train.json")
VALIDATION_FILE = Path("training/nyaya_validation.json")
TEST_FILE = Path("training/nyaya_test.json")


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Make the split reproducible
    random.seed(42)
    random.shuffle(data)

    total = len(data)

    train_end = int(total * 0.80)
    validation_end = int(total * 0.90)

    train_data = data[:train_end]
    validation_data = data[train_end:validation_end]
    test_data = data[validation_end:]

    with open(TRAIN_FILE, "w", encoding="utf-8") as file:
        json.dump(train_data, file, indent=2, ensure_ascii=False)

    with open(VALIDATION_FILE, "w", encoding="utf-8") as file:
        json.dump(validation_data, file, indent=2, ensure_ascii=False)

    with open(TEST_FILE, "w", encoding="utf-8") as file:
        json.dump(test_data, file, indent=2, ensure_ascii=False)

    print("Dataset split completed.")
    print("------------------------")
    print(f"Total:      {len(data)}")
    print(f"Training:   {len(train_data)}")
    print(f"Validation: {len(validation_data)}")
    print(f"Test:       {len(test_data)}")


if __name__ == "__main__":
    main()