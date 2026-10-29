from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

def main():
    print("Loading Qwen 0.5B...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a logical reasoning assistant. "
                "Return only valid JSON."
            )
        },
        {
            "role": "user",
            "content": """
Solve this logical problem using the six Nyaya stages.

Premises:
All researchers are curious.
Ravi is a researcher.

Question:
Is Ravi curious?

Return JSON with exactly these fields:
samshaya
pramana
pancha_avayava
tarka
hetvabhasa
nirnaya
conclusion

The conclusion must contain:
subject
predicate
truth
"""
        }
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(prompt, return_tensors="pt")

    print("Generating...")

    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        do_sample=False
    )

    generated = outputs[0][inputs["input_ids"].shape[1]:]

    response = tokenizer.decode(
        generated,
        skip_special_tokens=True
    )

    print("\n===== QWEN 0.5B OUTPUT =====")
    print(response)


if __name__ == "__main__":
    main()
    