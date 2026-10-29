from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    return tokenizer, model


def generate_nyaya_reasoning(problem, max_new_tokens=350):
    tokenizer, model = load_model()

    messages = [
        {
            "role": "system",
            "content": (
                "You are a logical reasoning assistant. "
                "Return ONLY valid JSON. "
                "Never return markdown or explanatory text outside the JSON."
            )
        },
        {
            "role": "user",
            "content": f"""
Solve this logical problem using the six Nyaya stages.

Return exactly these JSON fields:

samshaya
pramana
pancha_avayava
tarka
hetvabhasa
nirnaya
conclusion

The pancha_avayava object must contain exactly:

pratijna
hetu
udaharana
upanaya
nigamana

The conclusion object must contain exactly:

subject
predicate
truth

Rules for conclusion:
- subject = the entity being evaluated.
- predicate = the property being evaluated.
- truth = true if the premises logically establish the predicate.
- truth = false if the premises logically establish that the predicate is false.
- If the premises do not determine the answer, truth must be null.
- Do not guess.
- The conclusion field must represent the actual logical answer, not an explanation.

Logical problem:

{problem}
"""
        }
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False
    )

    input_length = inputs["input_ids"].shape[1]
    generated_tokens = outputs[0][input_length:]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return response


if __name__ == "__main__":
    problem = """
All researchers are curious.
Ravi is a researcher.
Is Ravi curious?
"""

    answer = generate_nyaya_reasoning(problem)
    print(answer)