from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE_MODEL = "distilgpt2"
ADAPTER_PATH = "models/nyaya_distilgpt2_lora"

PROMPT = """Solve the logical problem.

Premises:
All researchers are curious.
Ravi is a researcher.

Question:
Is Ravi curious?

Answer:
"""


def generate(model, tokenizer):
    inputs = tokenizer(PROMPT, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=30,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    )

    return tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )


def main():
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("\nLoading BASE model...")
    base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)

    print("Generating BASE output...")
    base_output = generate(base_model, tokenizer)

    print("\nLoading TRAINED LoRA model...")
    trained_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)
    trained_model = PeftModel.from_pretrained(
        trained_model,
        ADAPTER_PATH
    )

    print("Generating TRAINED output...")
    trained_output = generate(trained_model, tokenizer)

    print("\n===== BASE MODEL =====")
    print(base_output)

    print("\n===== TRAINED MODEL =====")
    print(trained_output)


if __name__ == "__main__":
    main()