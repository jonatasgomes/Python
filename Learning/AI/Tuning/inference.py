from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch
import warnings

# Suppress the pad_token_id warning
warnings.filterwarnings("ignore", message=".*pad_token_id.*")

# M1 Mac: Use Metal Performance Shaders (MPS) instead of CPU
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("✓ Using Apple Metal Performance Shaders (MPS)")
else:
    device = torch.device("cpu")
    print("✓ Using CPU (MPS not available)")

# Load base model
print("Loading base model...")
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token  # Set pad token to avoid warning
base_model = AutoModelForCausalLM.from_pretrained(model_name)
base_model.config.pad_token_id = tokenizer.pad_token_id  # Set in model config

# Load your fine-tuned LoRA weights
print("Loading LoRA weights...")
model = PeftModel.from_pretrained(base_model, "./model_lora")
model.to(device)
model.eval()

# Test prompts
test_prompts = [
    "The capital of France is",
    "The Eiffel Tower is located in",
    "France is famous for",
]

print("\n" + "="*80)
print("RUNNING FINE-TUNED MODEL LOCALLY ON M1 MAC")
print("="*80 + "\n")

for prompt in test_prompts:
    print(f"Prompt: '{prompt}'")
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    with torch.no_grad():
        output = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=60,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            pad_token_id=tokenizer.eos_token_id
        )
    
    result = tokenizer.decode(output[0], skip_special_tokens=True)
    print(f"Output: {result}\n")

print("="*80)
print("✓ Done!")