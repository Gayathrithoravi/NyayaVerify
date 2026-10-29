from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import LoraConfig, get_peft_model


MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

DATA_FILE = "training/nyaya_folio_train.jsonl"

OUTPUT_DIR = "models/nyaya_qwen_lora"

MAX_EXAMPLES = 150


def main():

    print("=" * 60)
    print("NYAYAVERIFY - FAST QWEN LORA TRAINING")
    print("=" * 60)

    # --------------------------------------------------
    # TOKENIZER
    # --------------------------------------------------

    print("\nLoading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # --------------------------------------------------
    # MODEL
    # --------------------------------------------------

    print("\nLoading Qwen 1.5B...")

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME
    )

    # --------------------------------------------------
    # LORA
    # --------------------------------------------------

    print("\nApplying LoRA...")

    lora_config = LoraConfig(
        r=4,
        lora_alpha=8,
        lora_dropout=0.05,
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
        ],
        bias="none",
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(
        model,
        lora_config
    )

    model.print_trainable_parameters()

    # --------------------------------------------------
    # DATASET
    # --------------------------------------------------

    print("\nLoading FOLIO/Nyaya dataset...")

    dataset = load_dataset(
        "json",
        data_files=DATA_FILE,
        split="train",
    )

    print(
        f"Original examples: {len(dataset)}"
    )

    # --------------------------------------------------
    # SMALL CPU-FRIENDLY SUBSET
    # --------------------------------------------------

    dataset = dataset.select(
        range(
            min(
                MAX_EXAMPLES,
                len(dataset)
            )
        )
    )

    print(
        f"Training examples selected: {len(dataset)}"
    )

    # --------------------------------------------------
    # TOKENIZATION
    # --------------------------------------------------

    def tokenize(example):

        return tokenizer(
            example["text"],
            truncation=True,
            max_length=256,
        )

    print("\nTokenizing...")

    tokenized_dataset = dataset.map(
        tokenize,
        batched=True,
        remove_columns=dataset.column_names,
    )

    # --------------------------------------------------
    # TRAINING SETTINGS
    # --------------------------------------------------

    training_args = TrainingArguments(

        output_dir=OUTPUT_DIR,

        num_train_epochs=1,

        per_device_train_batch_size=1,

        gradient_accumulation_steps=1,

        learning_rate=2e-4,

        logging_steps=10,

        save_strategy="no",

        report_to="none",

        fp16=False,

        bf16=False,

        dataloader_pin_memory=False,

        use_cpu=True,

        optim="adamw_torch",

    )

    # --------------------------------------------------
    # DATA COLLATOR
    # --------------------------------------------------

    data_collator = DataCollatorForLanguageModeling(

        tokenizer=tokenizer,

        mlm=False,

    )

    # --------------------------------------------------
    # TRAINER
    # --------------------------------------------------

    trainer = Trainer(

        model=model,

        args=training_args,

        train_dataset=tokenized_dataset,

        data_collator=data_collator,

    )

    # --------------------------------------------------
    # TRAIN
    # --------------------------------------------------

    print("\nStarting Qwen LoRA training...")

    trainer.train()

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    print("\nSaving LoRA adapter...")

    trainer.save_model(
        OUTPUT_DIR
    )

    tokenizer.save_pretrained(
        OUTPUT_DIR
    )

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)

    print(
        f"\nAdapter saved to:\n{OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()