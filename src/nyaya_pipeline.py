import sys

sys.path.insert(0, "src")

from llm_reasoner import generate_nyaya_reasoning
from json_parser import parse_model_output
from validator import validate_structure
from z3_verifier import verify_from_reasoning


def run_nyaya_pipeline(problem):
    # Step 1: Generate reasoning with Qwen
    raw_response = generate_nyaya_reasoning(problem)

    # Step 2: Parse JSON
    parsed = parse_model_output(raw_response)

    if not parsed["success"]:
        return {
            "llm_output": raw_response,
            "json_valid": False,
            "structure_valid": False,
            "logic_valid": False,
            "error": parsed["error"]
        }

    reasoning = parsed["data"]

    # Step 3: Validate Nyaya structure
    structure_result = validate_structure(reasoning)

    # Step 4: Verify Qwen's actual conclusion with Z3
    logic_result = verify_from_reasoning(reasoning)

    return {
        "llm_output": reasoning,
        "json_valid": True,
        "structure_valid": structure_result["valid"],
        "logic_valid": logic_result["valid"],
        "validation": structure_result,
        "logic_verification": logic_result
    }


if __name__ == "__main__":
    problem = """
All researchers are curious.
Ravi is a researcher.
Is Ravi curious?
"""

    result = run_nyaya_pipeline(problem)

    print("\n===== NYAYAVERIFY RESULT =====")
    print(result)