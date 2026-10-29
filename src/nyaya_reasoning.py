import json

from src.llm_reasoner import load_model


def create_nyaya_reasoning(problem):
    """
    Generate a six-stage Nyaya reasoning structure
    using the local Qwen model.
    """

    tokenizer, model = load_model()

    messages = [
        {
            "role": "system",
            "content": (
                "You are a logical reasoning assistant inspired by "
                "Navya-Nyaya.\n\n"

                "Return ONLY valid JSON. "
                "Do not return markdown or explanations outside JSON.\n\n"

                "The JSON must contain exactly these fields:\n"
                "samshaya\n"
                "pramana\n"
                "pancha_avayava\n"
                "tarka\n"
                "hetvabhasa\n"
                "nirnaya\n"
                "conclusion\n\n"

                "IMPORTANT:\n"
                "pancha_avayava MUST ALWAYS be a JSON OBJECT, "
                "never a list.\n\n"

                "The pancha_avayava object must contain exactly:\n"
                "pratijna\n"
                "hetu\n"
                "udaharana\n"
                "upanaya\n"
                "nigamana\n\n"

                "The reasoning stages mean:\n"
                "1. samshaya = identify the doubt or question.\n"
                "2. pramana = identify the evidence from the premises.\n"
                "3. pancha_avayava = construct the five-part argument.\n"
                "4. tarka = perform a counter-check or contradiction check.\n"
                "5. hetvabhasa = check whether the reasoning contains a fallacy.\n"
                "6. nirnaya = state the reasoned conclusion.\n"
                "7. conclusion = state the final answer clearly.\n\n"

                "For pancha_avayava:\n"
                "- pratijna = proposition to be established.\n"
                "- hetu = reason.\n"
                "- udaharana = supporting example or general rule.\n"
                "- upanaya = application of the rule to the case.\n"
                "- nigamana = final inference.\n"
            )
        },
        {
            "role": "user",
            "content": f"Logical problem:\n{problem}"
        }
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=500,
        do_sample=False
    )

    input_length = inputs["input_ids"].shape[1]

    generated_tokens = outputs[0][input_length:]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    ).strip()

    # Remove accidental markdown fences
    if response.startswith("```"):
        response = response.replace(
            "```json",
            ""
        )
        response = response.replace(
            "```",
            ""
        )
        response = response.strip()

    try:

        reasoning = json.loads(response)

    except json.JSONDecodeError:

        # Safe fallback if Qwen does not return valid JSON.
        reasoning = {
            "problem": problem,
            "samshaya": response,
            "pramana": "",
            "pancha_avayava": {
                "pratijna": "",
                "hetu": "",
                "udaharana": "",
                "upanaya": "",
                "nigamana": ""
            },
            "tarka": "",
            "hetvabhasa": "",
            "nirnaya": "",
            "conclusion": ""
        }

    # --------------------------------------------------
    # NORMALIZE THE MODEL OUTPUT
    # --------------------------------------------------

    # Keep original problem
    reasoning["problem"] = problem

    # Required top-level fields
    reasoning.setdefault(
        "samshaya",
        ""
    )

    reasoning.setdefault(
        "pramana",
        ""
    )

    reasoning.setdefault(
        "tarka",
        ""
    )

    reasoning.setdefault(
        "hetvabhasa",
        ""
    )

    reasoning.setdefault(
        "nirnaya",
        ""
    )

    reasoning.setdefault(
        "conclusion",
        ""
    )

    # --------------------------------------------------
    # FIX PANCHA AVAYAVA
    # --------------------------------------------------

    pancha = reasoning.get(
        "pancha_avayava"
    )

    # Qwen sometimes returns a list instead of an object.
    # Convert that safely into the required structure.
    if not isinstance(pancha, dict):

        reasoning["pancha_avayava"] = {
            "pratijna": "",
            "hetu": "",
            "udaharana": "",
            "upanaya": "",
            "nigamana": ""
        }

    # Ensure every required Pancha Avayava field exists.
    for field in [
        "pratijna",
        "hetu",
        "udaharana",
        "upanaya",
        "nigamana"
    ]:

        reasoning["pancha_avayava"].setdefault(
            field,
            ""
        )

    return reasoning


def process_problem(problem):

    from src.validator import validate_structure

    reasoning = create_nyaya_reasoning(
        problem
    )

    validation_result = validate_structure(
        reasoning
    )

    return {
        "reasoning": reasoning,
        "validation": validation_result
    }


if __name__ == "__main__":

    problem = (
        "Every researcher is curious. "
        "Ravi is a researcher. "
        "Is Ravi curious?"
    )

    result = process_problem(
        problem
    )

    print(
        "NYAYA REASONING"
    )

    print(
        result["reasoning"]
    )

    print(
        "\nVALIDATION RESULT"
    )

    print(
        result["validation"]
    )