import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.fol_parser import parse_formula
from src.z3_verifier import verify_logic


def main():

    fact_formula = "Student(rina)"

    parsed = parse_formula(fact_formula)

    result = verify_logic(
        facts=[parsed["value"]],
        rules=[],
        query="curious_rina"
    )

    print("===== UNKNOWN FOL → PARSER → Z3 =====")
    print("FOL:", fact_formula)
    print("Parsed:", parsed)
    print("Query: curious_rina")
    print("Result:", result)


if __name__ == "__main__":
    main()