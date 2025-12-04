from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch
import warnings
import os

# Suppress all transformers warnings
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
warnings.filterwarnings("ignore")

# M1 Mac: Use Metal Performance Shaders (MPS) instead of CPU
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("✓ Using Apple Metal Performance Shaders (MPS)\n")
else:
    device = torch.device("cpu")
    print("✓ Using CPU (MPS not available)\n")

print("Loading model...")
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
base_model = AutoModelForCausalLM.from_pretrained(model_name)
base_model.config.pad_token_id = tokenizer.pad_token_id

print("Loading LoRA weights...")
model = PeftModel.from_pretrained(base_model, "./model_lora")
model.to(device)
model.eval()

print("✓ Model loaded! Type 'quit' to exit.\n")
print("="*80)

while True:
    prompt = input("\nYou: ")
    
    if prompt.lower() == "quit":
        print("\nGoodbye!")
        break
    
    if not prompt.strip():
        continue
    
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    with torch.no_grad():
        output = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=100,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            pad_token_id=tokenizer.eos_token_id
        )
    
    result = tokenizer.decode(output[0], skip_special_tokens=True)
    print(f"\nModel: {result}")
    print("-"*80)