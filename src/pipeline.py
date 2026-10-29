from src.nyaya_reasoning import create_nyaya_reasoning
from src.validator import validate_structure
from src.conclusion_formalizer import formalize_conclusion
from src.fol_parser import parse_formula
from src.z3_verifier import verify_formulas


def run_pipeline(problem, conclusion, premises_fol, premises_text=None):

    # --------------------------------------------------
    # 1. Prepare problem for Nyaya reasoning
    # --------------------------------------------------
    nyaya_problem = (
        f"Premises:\n{premises_text if premises_text else premises_fol}\n\n"
        f"Conclusion:\n{conclusion}"
    )

    # --------------------------------------------------
    # 2. Generate six-stage Nyaya reasoning
    # --------------------------------------------------
    reasoning = create_nyaya_reasoning(nyaya_problem)

    # --------------------------------------------------
    # 3. Validate Nyaya reasoning structure
    # --------------------------------------------------
    structure_result = validate_structure(reasoning)

    # --------------------------------------------------
    # 4. Convert English conclusion into FOL
    #    using natural-language + FOL premises
    # --------------------------------------------------
    formalized_conclusion = formalize_conclusion(
        conclusion,
        premises_fol,
        premises_text
    )

    # --------------------------------------------------
    # 5. Parse premises and conclusion
    # --------------------------------------------------
    parsed_premises = [
        parse_formula(premise)
        for premise in premises_fol
    ]

    parsed_conclusion = parse_formula(
        formalized_conclusion
    )

    # --------------------------------------------------
    # 6. Verify using Z3
    # --------------------------------------------------
    verification_result = verify_formulas(
        parsed_premises,
        parsed_conclusion
    )

    # --------------------------------------------------
    # 7. Return complete result
    # --------------------------------------------------
    return {
        "problem": problem,
        "reasoning": reasoning,
        "structure_validation": structure_result,
        "english_conclusion": conclusion,
        "formalized_conclusion": formalized_conclusion,
        "logical_verification": verification_result
    }


if __name__ == "__main__":

    import ast
    import csv

    with open(
        "data/folio-train.txt",
        encoding="utf-8"
    ) as f:

        rows = list(
            csv.DictReader(
                f,
                delimiter="\t"
            )
        )

    row = rows[9]

    premises_fol = ast.literal_eval(
        row["premises-FOL"]
    )

    result = run_pipeline(
        problem=(
            "Determine whether the conclusion "
            "follows from the given premises."
        ),
        conclusion=row["conclusion"],
        premises_fol=premises_fol,
        premises_text=row["premises"]
    )

    print(
        "\n========== NYAYAVERIFY PIPELINE ==========\n"
    )

    print("CONCLUSION:")
    print(result["english_conclusion"])

    print("\nFORMALIZED CONCLUSION:")
    print(result["formalized_conclusion"])

    print("\nSTRUCTURE VALIDATION:")
    print(result["structure_validation"])

    print("\nLOGICAL VERIFICATION:")
    print(result["logical_verification"])

    print("\nNYAYA REASONING:")
    print(result["reasoning"])

    print("\nFOLIO LABEL:")
    print(row["label"])