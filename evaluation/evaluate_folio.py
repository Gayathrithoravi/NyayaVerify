import ast
import csv
import sys
import os
import traceback


# Add project root to Python path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from src.pipeline import run_pipeline


def load_folio_data(path):
    with open(path, encoding="utf-8") as f:
        return list(
            csv.DictReader(
                f,
                delimiter="\t"
            )
        )


def normalize_label(label):
    return label.strip().lower()


def main():

    data = load_folio_data(
        "data/folio-train.txt"
    )

    # Start with only 10 examples
    test_data = data[:10]

    correct = 0
    total = len(test_data)

    print(
        "\n========== NYAYAVERIFY FOLIO EVALUATION ==========\n"
    )

    for i, row in enumerate(
        test_data,
        start=1
    ):

        print(
            f"\n----- Example {i}/{total} -----"
        )

        # Convert FOLIO string representation
        # into a Python list
        premises_fol = ast.literal_eval(
            row["premises-FOL"]
        )

        # Natural-language premises
        premises_text = row["premises"]

        conclusion = row["conclusion"]

        expected = normalize_label(
            row["label"]
        )

        try:

            result = run_pipeline(
                problem=(
                    "Determine whether the conclusion "
                    "follows from the given premises."
                ),
                conclusion=conclusion,
                premises_fol=premises_fol,
                premises_text=premises_text,
            )

            verification = result[
                "logical_verification"
            ]

            if verification["truth"] is True:

                predicted = "true"

            elif verification["truth"] is False:

                predicted = "false"

            else:

                predicted = "unknown"

            is_correct = (
                predicted == expected
            )

            if is_correct:
                correct += 1

            print(
                "Conclusion :",
                conclusion
            )

            print(
                "Expected   :",
                expected
            )

            print(
                "Predicted  :",
                predicted
            )

            print(
                "Correct    :",
                is_correct
            )

        except Exception as e:

            print(
                "\nERROR:",
                e
            )

            print(
                "\n========== FULL TRACEBACK =========="
            )

            traceback.print_exc()

            print(
                "====================================\n"
            )

            print(
                "Expected:",
                expected
            )

            print(
                "Predicted: error"
            )

    accuracy = (
        correct / total
    ) * 100

    print(
        "\n========== RESULTS =========="
    )

    print(
        f"Correct : {correct}/{total}"
    )

    print(
        f"Accuracy: {accuracy:.2f}%"
    )

    print(
        "=============================\n"
    )


if __name__ == "__main__":

    main()