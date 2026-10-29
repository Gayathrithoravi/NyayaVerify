import json
import re


def parse_model_output(response):
    response = response.strip()

    # Try direct JSON parsing first.
    try:
        data = json.loads(response)

        return {
            "success": True,
            "data": data,
            "error": None
        }

    except json.JSONDecodeError:
        pass

    # Try to find a JSON object inside the response.
    match = re.search(r"\{.*\}", response, re.DOTALL)

    if match:
        try:
            data = json.loads(match.group(0))

            return {
                "success": True,
                "data": data,
                "error": None
            }

        except json.JSONDecodeError:
            pass

    return {
        "success": False,
        "data": None,
        "error": "Model response does not contain valid JSON."
    }


if __name__ == "__main__":
    test_response = '{"samshaya": "Is Ravi curious?", "nirnaya": "Ravi is curious."}'

    result = parse_model_output(test_response)

    print(result)