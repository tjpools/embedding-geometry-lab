"""
Experiment 01 — First Local Inference
======================================
Model:   TinyLlama-1.1B-Chat-v1.0
         1.1 billion parameters (~2.2GB download)
         No license gate — public model, no special approval needed

What this experiment maps:
  - Download: how HF token + huggingface_hub pulls weights to local cache
  - Load time: how long it takes to deserialize weights into RAM
  - Inference: how long a single forward pass takes on CPU
  - RAM usage: how much system memory the model occupies
  - Output: what the model actually says

This is the first geodesic through the manifold.
Every number printed here is a real measurement of your hardware.
"""

import time
import os
import psutil
from dotenv import load_dotenv

# ── 1. Load the boundary condition (HF token) ─────────────────────────────────
load_dotenv('/home/tjpools/AiProjectIntel/.env')
token = os.getenv('HUGGINGFACE_TOKEN') or os.getenv('HF_TOKEN')
print(f"[boundary] HF token loaded: {'yes' if token else 'NO — check .env'}")

# ── 2. Import the transformer stack ───────────────────────────────────────────
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# ── 3. Download + load the model ──────────────────────────────────────────────
print(f"\n[load] Fetching weights for {MODEL_ID}")
print("       (first run: ~2.2GB download — subsequent runs load from cache)")

ram_before = psutil.Process().memory_info().rss / 1e9
t_load_start = time.time()

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token=token)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[device] Using: {device.upper()}", end="")
if device == "cuda":
    print(f" ({torch.cuda.get_device_name(0)}, "
          f"{round(torch.cuda.get_device_properties(0).total_memory/1e9,2)} GB VRAM)")
else:
    print()

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    token=token,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    low_cpu_mem_usage=True,
)
model.to(device)
model.eval()

t_load_end = time.time()
ram_after = psutil.Process().memory_info().rss / 1e9

print(f"[load] Done in {t_load_end - t_load_start:.1f}s")
print(f"[ram]  Model occupies ~{ram_after - ram_before:.2f} GB of system RAM")
print(f"[ram]  Total process RAM: {ram_after:.2f} GB")

# ── 4. Run inference ───────────────────────────────────────────────────────────
PROMPT = "What are three things to do in Paris?"

# TinyLlama uses a chat template — wrap the prompt correctly
messages = [{"role": "user", "content": PROMPT}]
input_text = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)

inputs = tokenizer(input_text, return_tensors="pt").to(device)
input_tokens = inputs["input_ids"].shape[1]

print(f"\n[inference] Prompt: '{PROMPT}'")
print(f"[inference] Input tokens: {input_tokens}")
print("[inference] Generating...")

t_infer_start = time.time()
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        do_sample=False,          # greedy decode — deterministic, faster
        pad_token_id=tokenizer.eos_token_id,
    )
t_infer_end = time.time()

# ── 5. Decode and report ───────────────────────────────────────────────────────
output_tokens = outputs.shape[1] - input_tokens
elapsed = t_infer_end - t_infer_start
tokens_per_sec = output_tokens / elapsed

response = tokenizer.decode(outputs[0][input_tokens:], skip_special_tokens=True)

print(f"\n{'─'*60}")
print(response)
print(f"{'─'*60}")
print(f"\n[metrics] Output tokens:  {output_tokens}")
print(f"[metrics] Inference time: {elapsed:.1f}s")
print(f"[metrics] Throughput:     {tokens_per_sec:.1f} tokens/sec")
print(f"[metrics] Device:         {device.upper()} ({torch.cuda.get_device_name(0) if device == 'cuda' else 'no GPU'})")
print("\n[done] First geodesic complete. Record these numbers in notes/boundary-map.md")
