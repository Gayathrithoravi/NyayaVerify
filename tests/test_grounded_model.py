from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE_MODEL = "distilgpt2"
ADAPTER_PATH = "models/nyaya_grounded_test"

PROMPT = """Solve the logical problem using the six Nyaya stages.

Premises:
All people who regularly drink coffee are dependent on caffeine.
People either regularly drink coffee or joke about being addicted to caffeine.
No one who jokes about being addicted to caffeine is unaware that caffeine is a drug.
Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug.

Question:
Rina is a person who jokes about being addicted to caffeine or unaware that caffeine is a drug.

Answer:
"""


def main():
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("Loading base model...")
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)

    print("Loading grounded LoRA adapter...")
    model = PeftModel.from_pretrained(model, ADAPTER_PATH)

    inputs = tokenizer(PROMPT, return_tensors="pt")

    print("Generating grounded response...")

    outputs = model.generate(
        **inputs,
        max_new_tokens=250,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    )

    response = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    print("\n===== GROUNDED TRAINED MODEL =====")
    print(response)


if __name__ == "__main__":
    main()