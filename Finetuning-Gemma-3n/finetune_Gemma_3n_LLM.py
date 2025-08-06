"""
Author: SURYA DEEP SINGH
LinkedIn: https://www.linkedin.com/in/surya-deep-singh-b9b94813a/
Medium: https://medium.com/@SuryaDeepSingh
GitHub: https://github.com/SinghSuryaDeep
"""
import torch
import json
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import Dataset
from trl import SFTTrainer
import time

print("🚀 Starting EmpowerEd Gemma-3n 2B Fine-tuning for Special Needs Education")
print(f"Device: {'MPS' if torch.backends.mps.is_available() else 'CPU'}")

MODEL_NAME = 'google/gemma-3n-E2B'
OUTPUT_DIR = "./models/empowered-gemma-3n-2b"
MERGED_OUTPUT_DIR = "./models/empowered-gemma-3n-2b-merged"

device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
torch_dtype = torch.float16

print(f"Using model: {MODEL_NAME}")
print(f"Using dtype {torch_dtype} on device {device}")

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch_dtype,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
) if not torch.backends.mps.is_available() else None

try:
    print("Loading Gemma-3n 2B model for EmpowerEd... (this may take a few minutes)")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch_dtype,
        device_map={"": device} if torch.backends.mps.is_available() else "auto",
        trust_remote_code=True,
        quantization_config=quantization_config,
        low_cpu_mem_usage=True,
    )

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("Preparing model for LoRA...")
    model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=[
            "q_proj",
            "k_proj", 
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj"
        ],
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, lora_config)
    print("LoRA configuration applied successfully!")
    model.print_trainable_parameters()

    # Load pre-existing training examples from the JSON file
    print("Loading pre-existing training examples from 'data/empowered_training_examples.json'...")

    with open("data/empowered_training_examples.json", "r") as f:
        all_training_examples = json.load(f)

    # Format dataset examples
    formatted_dataset = [{"text": f"<start_of_turn>user\n{ex['instruction']}<end_of_turn>\n<start_of_turn>model\n{ex['output']}<end_of_turn>"} for ex in all_training_examples]
    dataset = Dataset.from_list(formatted_dataset)
    print(f"Training dataset created with {len(dataset)} examples")

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=1,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        gradient_checkpointing=True,
        optim="adamw_torch",
        logging_steps=10,
        save_strategy="epoch",
        learning_rate=2e-4,
        bf16=False,
        max_grad_norm=0.3,
        warmup_ratio=0.1,
        lr_scheduler_type="cosine",
        dataloader_drop_last=True,
        remove_unused_columns=False,
        report_to="none",
        save_total_limit=2,
        dataloader_num_workers=0,
        push_to_hub=False,
    )

    print("Creating SFT trainer...")
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
    )

    print("🎓 Starting EmpowerEd model training...")
    start_time = time.time()
    trainer.train()
    training_time = time.time() - start_time
    print(f"⏱️ Training completed in {training_time/60:.1f} minutes")

    print("💾 Saving LoRA adapters...")
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    print("🔧 Merging LoRA adapters with base model...")
    from peft import PeftModel

    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch_dtype,
        device_map={"": device} if torch.backends.mps.is_available() else "auto",
        trust_remote_code=True,
    )

    peft_model = PeftModel.from_pretrained(base_model, OUTPUT_DIR)
    merged_model = peft_model.merge_and_unload()

    os.makedirs(MERGED_OUTPUT_DIR, exist_ok=True)
    merged_model.save_pretrained(MERGED_OUTPUT_DIR)
    tokenizer.save_pretrained(MERGED_OUTPUT_DIR)

    print(f"✅ EmpowerEd model training complete!")
    print(f"📁 LoRA adapters: {OUTPUT_DIR}")
    print(f"📁 Merged model: {MERGED_OUTPUT_DIR}")

    print("\n📖 Next Steps:")
    print("1. Convert to GGUF format for Ollama deployment")
    print("2. Create Ollama Modelfile and build the model")
    print("3. Test with your Streamlit app")
    print("4. Consider quantization for better performance")
    
    print("🚀 EmpowerEd model is now ready!")
except Exception as e:
    print(f"❌ Error encountered: {str(e)}")
