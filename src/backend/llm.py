# llm.py
import sys
import subprocess
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM

try:
    import torch_directml
    directml_available = True
except ImportError:
    directml_available = False

def check_hardware_type(model_name):
    """Detect hardware and return tokenizer, model, and device"""
    is_seq2seq = "flan-t5" in model_name.lower()

    # check NVIDIA GPU
    try:
        subprocess.check_output("nvidia-smi", shell=True)
        print("NVIDIA GPU detected")
        return run_model_nvidia_gpu(model_name)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("No NVIDIA GPU detected (nvidia-smi failed or not found)")

    # check AMD GPU with DirectML (avoid for seq2seq due to bug)
    if directml_available and torch_directml.is_available() and not is_seq2seq:
        print("AMD GPU detected with DirectML support")
        return run_model_amd_gpu(model_name)

    # fallback to CPU
    print("Falling back to CPU" + (" (DirectML incompatible with seq2seq)" if is_seq2seq else ""))
    return run_model_cpu(model_name)

def run_model_nvidia_gpu(model_name):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Loading {model_name} on {device}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = (AutoModelForSeq2SeqLM.from_pretrained(model_name) if "flan-t5" in model_name.lower()
             else AutoModelForCausalLM.from_pretrained(model_name)).to(device)
    return tokenizer, model, device

def run_model_amd_gpu(model_name):
    device = torch_directml.device() if directml_available else torch.device("cpu")
    print(f"Loading {model_name} on {device}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)  # Causal only
    return tokenizer, model, device

def run_model_cpu(model_name):
    device = torch.device("cpu")
    print(f"Loading {model_name} on {device}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = (AutoModelForSeq2SeqLM.from_pretrained(model_name) if "flan-t5" in model_name.lower()
             else AutoModelForCausalLM.from_pretrained(model_name)).to(device)
    return tokenizer, model, device

if __name__ == "__main__":
    model_name = "google/flan-t5-base"
    tokenizer, model, device = check_hardware_type(model_name)

    print(f"Running on {device} (Ryzen 7 3700X or GPU)")
    print("\nType your prompt (or 'exit' to quit):")
    while True:
        prompt = input("Prompt> ")
        if prompt.lower() == "exit":
            print("Goodbye!")
            sys.exit(0)
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        outputs = model.generate(inputs["input_ids"], max_length=100, num_beams=4 if "flan-t5" in model_name.lower() else 1, do_sample=False)
        print(f"Response: {tokenizer.decode(outputs[0], skip_special_tokens=True)}\n")