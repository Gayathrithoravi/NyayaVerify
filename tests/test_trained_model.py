from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


BASE_MODEL = "distilgpt2"
ADAPTER_PATH = "models/nyaya_distilgpt2_lora"


def main():
    print("Loading base model...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("Loading trained LoRA adapter...")
    model = PeftModel.from_pretrained(
        model,
        ADAPTER_PATH
    )

    prompt = """Solve the logical problem using the six Nyaya stages.

Premises:
All researchers are curious.
Ravi is a researcher.

Question:
Is Ravi curious?

Answer:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    print("Generating response...")

    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    )

    response = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    print("\n===== TRAINED MODEL OUTPUT =====")
    print(response)


if __name__ == "__main__":
    main()